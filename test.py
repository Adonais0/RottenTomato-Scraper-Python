#_*_ coding: utf-8 _*_
import requests
import json
from bs4 import BeautifulSoup
import io
import sys
from selenium import webdriver
from urllib2 import quote
import csv
import time
# URL = "https://www.rottentomatoes.com/m/birth_of_the_dragon"

URL = "https://www.rottentomatoes.com/m/all_saints"
big_url = "https://www.rottentomatoes.com/browse/dvd-streaming-all"
baseurl = "https://www.rottentomatoes.com"

class Movie:
    def __init__(self,soup):
        self.name = soup.find("h1").text.strip()
        self.genre = soup.find("ul",{"class":"content-meta info"}).find_all("li")[1].find("a").text.strip()
        self.director = soup.find("ul",{"class":"content-meta info"}).find_all("li")[2].find("a").text.strip()
        self.date = soup.find("ul",{"class":"content-meta info"}).find_all("li")[4].find_all("div")[1].text.strip()
        self.tomato_meter = soup.find("div",{"class":"critic-score meter"}).find("span", {"class": "superPageFontColor"}).find("span").text
        self.tomato_num =  soup.find("div",{"id":"scoreStats"}).find_all("div",{"class":"superPageFontColor"})[1].find_all("span")[1].text
        if soup.find("div",{"class":"audience-score meter"}).find("span",{"class":"superPageFontColor"}):
            self.audience_score = soup.find("div",{"class":"audience-score meter"}).find("span",{"class":"superPageFontColor"}).text.strip()
        else:
            self.audience_score = None
        self.audence_num = soup.find("div",{"class":"audience-info hidden-xs superPageFontColor"}).find_all("div")[1].text[-9:]
        try:
            self.boxoffice = soup.find("ul",{"class":"content-meta info"}).find_all("li")[6].find_all("div")[1].text.strip()
        except:
            self.boxoffice = "None"
    def __str__(self):
        return str(self.name+self.tomato_meter)
    def __repr__(self):
        try:
            r = "Name of Movie: {}\nTomato meter: {}\n".format(self.name,self.tomato_meter)
        except UnicodeEncodeError:#fix later
            r = "Unicode error here \n"
            # if sys.version_info>=(3,):
            #     r = ("Name of Movie: {}\nTomato meter: {}\n".format(self.name,self.tomato_meter)).decode('utf-8').decode(sys.stout.encoding)
            # else:
            #     r = ("Name of Movie: {}\nTomato meter: {}\n".format(self.name,self.tomato_meter)).decode('utf-16')
        return r
    def __contains__(self, item):
        return self.name.find(item)
def Cache(url,filename):#(L'ÉCONOMIE DU COUPLE)
    try:
        data = open(filename,'r').read()
    except:
        data = requests.get(url).text
        f = io.open(filename,'w',encoding='utf8')
        f.write(data)
        f.close()
    return data

testdata = Cache(URL,"movie.html")
# print(testdata)
#div class = critic-score meter, audience-score meter
soup = BeautifulSoup(testdata,'html.parser')
# dyna = Cache_dynamic(big_url,"movies.html")

#build cache of the url
def Cache_url_list(num):
    try:
        f = open('url.csv','r')
        cs = csv.reader(f)
        url_list = []
        for row in cs:
            url_list.append(row)
    except:
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
        wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
        for url in url_list:
            wr.writerow([url])
    return url_list

url_list = Cache_url_list(2000)
movie_list = []

# scrape single movie content
for url in url_list:
    print(url)
#     data = Cache(url,url[33:]+".html")
#     soup = BeautifulSoup(data,'html.parser')
#     movie_list.append(Movie(soup))
# print(movie_list)


# all_saints = Movie(soup)
# print(all_saints)
# print(all_saints.tomato_meter)
# print("all" in all_saints)
