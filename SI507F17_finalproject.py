#_*_ coding: utf-8 _*_
import requests
import json
from bs4 import BeautifulSoup
import io
import sys
from selenium import webdriver
import urllib.request as urllib2
import csv
import time
from config import *
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import plotly
from plotly.graph_objs import Scatter,Box, Layout
import plotlyconfig as config_pl

CACHE_FNAME = "cache_contents.json"
URL = "https://www.rottentomatoes.com/m/all_saints"
big_url = "https://www.rottentomatoes.com/browse/dvd-streaming-all"
baseurl = "https://www.rottentomatoes.com"

#Complex Cache System-----------------
try:
    f = open('cache_contents.json')
    text = f.read()
    CACHE_DICTION = json.loads(text)#turn text into python object
except:
    CACHE_DICTION = {}

def get_from_cache(url,dictionary):
    if url in dictionary: #dictionary of dictionary
        data = dictionary[url]
    else:
        data = None #Identifier not in dictionary
    return data #return data from dictionary['identifier']['values']

def set_in_data_cache(url, data):
    CACHE_DICTION[url]=data
    with open(CACHE_FNAME,'w') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)#turn CACHE_DICTION into json file
        cache_file.write(cache_json)

def get_data(url):
    data = get_from_cache(url,CACHE_DICTION)
    if data:
        print("getting data from cache...")
    else:
        print("requesting data from internet...")
        data = requests.get(url).text
        set_in_data_cache(url,data)
    return data

#------------------------------------
class Movie:
    def __init__(self,soup):
        try:
            self.name = soup.find("h1").text.strip()
        except:
            self.name = None
        try:
            self.genre = soup.find("ul",{"class":"content-meta info"}).find_all("li")[1].find("a").text.strip()
        except:
            self.genre = None
        try:
            self.director = soup.find("ul",{"class":"content-meta info"}).find_all("li")[2].find("a").text.strip()
        except:
            self.director = None
        try:
            self.date = soup.find("ul",{"class":"content-meta info"}).find_all("li")[4].find_all("div")[1].text.strip()
        except:
            self.date = None
        try:
            self.tomato_meter = int(soup.find("div",{"class":"critic-score meter"}).find("span", {"class": "superPageFontColor"}).find("span").text)
        except:
            self.tomato_meter = None
        try:
            self.tomato_num = int( soup.find("div",{"id":"scoreStats"}).find_all("div",{"class":"superPageFontColor"})[1].find_all("span")[1].text.replace(",",""))
        except:
            self.tomato_num = None
        try:
            self.audience_score = int(soup.find("div",{"class":"audience-score meter"}).find("span",{"class":"superPageFontColor"}).text.strip()[:-1].replace(",",""))
        except:
            self.audience_score = None
        try:
            self.audience_num = int(soup.find("div",{"class":"audience-info hidden-xs superPageFontColor"}).find_all("div")[1].text[-9:].replace(",",""))
        except:
            self.audience_num = None
        try:
            a = soup.find("ul",{"class":"content-meta info"}).find_all("li")[6].find_all("div")[1].text.strip()[1:]
            if "$" not in a:
                self.boxoffice = None
            self.boxoffice = int(a.replace(",", ""))
        except:
            self.boxoffice = None
    def __str__(self):
        return "\nMovie Name: "+self.name+"\n Meter: "+str(self.tomato_meter)
    def __repr__(self):
        return "\nMovie Name: "+self.name
    def __contains__(self, item):
        return self.name.find(item)

#Cache all the urls in URL.CSV
def Cache_url_list(num):
    try:
        print("get url from cache...")
        f = open('url.csv','r')
        cs = csv.reader(f)
        url_list = []
        i = 0
        for row in cs:#type of row is list
            url_list.append(row[0])
            print(row[0])
            i = i+1
            if i >=num:
                break
    except:
        print("get url from internet...")
        browser = webdriver.PhantomJS()
        browser.set_window_size(1120,550)
        browser.get(big_url)
        #selenium show more
        #use j define how many times you want to click show more button
        j = 0
        while j < 100:
            try:
                loadMoreButton = browser.find_element_by_xpath('//*[@id="show-more-btn"]/button')
                time.sleep(2)
                loadMoreButton.click()
                time.sleep(5)
                j = j+1
                print(j)
            except Exception as e:
                print (e)
                break

        m_soup = BeautifulSoup(browser.page_source,'html.parser')
        url_list = []
        for i in range(num):
            try:
                a = m_soup.find("div",{"class":"mb-movies"}).find_all("div",{"class":"mb-movie"})[i].find("a").get("href")
                url = baseurl+a
            except:
                url = "None"
            url_list.append(url)
        myfile = open ('url.csv','w')
        wr = csv.writer(myfile)
        x = 0
        for url in url_list:
            wr.writerow([url])#changed from([url])
            x = x+1
            print('write {} urls'.format(x))

    return url_list

# Create Movie list------------------
def return_movie_list(num):
    movie_list = []
    url_list = Cache_url_list(num)
    j = 0
    for url in url_list:
        data = get_data(url)
        soup = BeautifulSoup(data,'html.parser')
        movie_list.append(Movie(soup))
        j = j+1
        print("Finished requesting for {} movie.".format(j))
    return movie_list

#Get and Write data in csv file------------------------------
def get_data_from_csv(filename,list_movie):
    try:
        outfile = open(filename,"r")
        print("getting data from csv file...")
    except:
        print("setting data into csv file...")
        outfile = open(filename,"w")
        outfile.write("Name, Genre, Director, Date, TomatoMeter, TomatoMeterNum, AudienceScore, AudienceScoreNum, BoxOffice\n")
        for movie in list_movie:
            outfile.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(movie.name, movie.genre, movie.director,movie.date,movie.tomato_meter,movie.tomato_num,movie.audience_score,movie.audience_num,movie.boxoffice))#try python3
    return outfile

# movie_list = return_movie_list(2000)
movie_list = return_movie_list(5)
csv_file = get_data_from_csv('data.csv',movie_list)
#------------------------------------------------
#Connect with database--------------------------

#test would run 2000 data again using import
def get_connection_and_cursor():
    try:
        if db_password != "": #database has password
            db_connection = psycopg2.connect("dbname = '{0}' user='{1}' password='{2}'".format(db_name,db_user,db_password))
            print("connect successfully to database")
        else: #database doesn't have password
            db_connection = psycopg2.connect("dbname = '{0}' user='{1}'".format(db_name,db_user))
    except:
        print("Fail to connect to server")
        sys.exit(1)
    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, db_cursor
db_connection,db_cursor = get_connection_and_cursor()#connect to the database
def setup_database():
    #Table basic_info_of_movie
    try:
        db_cursor.execute("CREATE TABLE basic_info_of_movie(name VARCHAR(128) PRIMARY KEY,genre VARCHAR(128), director VARCHAR(255), time_in_theatre VARCHAR(128), boxoffice VARCHAR(255))")
    except:
        print("table already exists")
    #Table tomato_meter
    try:
        db_cursor.execute("CREATE TABLE tomato_meter(movie_id SERIAL PRIMARY KEY, name VARCHAR(128), tomato_meter INTEGER, tomato_num INTEGER, audience_score VARCHAR(255), audience_num VARCHAR(255), FOREIGN KEY (name) REFERENCES basic_info_of_movie(name))")
    except:
        print("table already exists")

    db_connection.commit()
    print('Setup database complete')

setup_database()#setup once

#------------INSERT INTO DATABASE------------------
def insert_into_database():
    with open ('data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        i = 0
        for row in reader:
            i = i+1
            if "404" not in row[0]:
                print("inputing into the database...")
                db_cursor.execute(
                    "INSERT INTO basic_info_of_movie VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", (row[0],row[1],row[2],row[3],row[4])
                )
                db_cursor.execute(
                    "INSERT INTO tomato_meter VALUES(%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", (i,row[0],row[4],row[5],row[6],row[7])
                    )
    db_connection.commit()
    print("successfully inserted")

insert_into_database()#insert once

def execute_and_print(query, numer_of_results=1):
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    for r in results[:numer_of_results]:
        print(r)
    print('--> Result Rows:', len(results))
    print()
    return results
#--------make query tests---------------
happy_movies = execute_and_print(""" SELECT "name" FROM "basic_info_of_movie" WHERE "genre" LIKE 'Comedy' """)
print(happy_movies)
a = execute_and_print(""" SELECT ("basic_info_of_movie"."director") FROM "basic_info_of_movie" INNER JOIN "tomato_meter" ON ("tomato_meter"."tomato_meter" = 100) """)
print(a)
meter = execute_and_print(' SELECT "name","tomato_meter","audience_score" FROM "tomato_meter"')
print(meter)
test = execute_and_print(""" SELECT * FROM "basic_info_of_movie" INNER JOIN "tomato_meter" ON "basic_info_of_movie"."name" = "tomato_meter"."name" """)
print(test)

#--------------VISUALIZATION---------------------
plotly.tools.set_credentials_file(username=config_pl.username, api_key=config_pl.api_key)

db_cursor.execute(""" SELECT * FROM "basic_info_of_movie" INNER JOIN "tomato_meter" ON "basic_info_of_movie"."name" = "tomato_meter"."name" """)
list_of_dict = db_cursor.fetchall()
list_of_genre = []
list_of_tomato_meter = []
list_of_audience_score = []
for d in list_of_dict:
    list_of_genre.append(d['genre'])
    list_of_tomato_meter.append(d['tomato_meter'])
    list_of_audience_score.append(d['audience_score'])
#-----------------------------------------
def show1():
    div = plotly.offline.plot({
        "data":[Scatter(x = list_of_tomato_meter, y = list_of_audience_score, mode = 'markers')],
        "layout": Layout(title = "Relation Between Tomato Meter and Audience Score",xaxis = dict(title = 'Tomato Meter'),yaxis = dict(title = 'Audience Score')),
    },
        filename = 'scatter.html')
    return div
show1()
def show2():
    div = plotly.offline.plot({
        "data":[Box(x = list_of_genre, y = list_of_tomato_meter, name = 'Tomato Meter'),Box(x = list_of_genre, y = list_of_audience_score, name = 'Audience Score')],
        "layout":Layout(title = "Relation Between Genre and Tomato Meter",boxmode = 'group'),
    },
        filename = 'box.html')
    return div
show2()
