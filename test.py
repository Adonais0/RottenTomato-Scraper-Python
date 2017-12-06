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

# URL = "https://www.rottentomatoes.com/m/birth_of_the_dragon"
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
            self.data = None
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
        return "\nMovie Name: "+self.name+"\n Meter: "+self.tomato_meter
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
        myfile = open ('url.csv','wb')
        wr = csv.writer(myfile)
        for url in url_list:
            wr.writerow([url])#changed from([url])
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

movie_list = return_movie_list(2000)
get_data_from_csv('data.csv',movie_list)
#------------------------------------------------
#Connect with database--------------------------

#------------------------------------------------
