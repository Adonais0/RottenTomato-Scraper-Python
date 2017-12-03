import requests
import json
from bs4 import BeautifulSoup
import io
import sys
from selenium import webdriver
from urllib2 import quote
# URL = "https://www.rottentomatoes.com/m/birth_of_the_dragon"

URL = "https://www.rottentomatoes.com/m/all_saints"
big_url = "https://www.rottentomatoes.com/browse/dvd-streaming-all"
browser = webdriver.PhantomJS()
browser.set_window_size(1120,550)
browser.get(big_url)

def search_artist(search_term, media_term = "all"):
    baseurl = "https://itunes.apple.com/search"
    params = {}
    params["media"] = media_term
    params["term"] = search_term

    # params["entity"] = entity
    result_dict = json.loads(requests.get(baseurl,params = params).text)
    return result_dict

class Media():
    def __init__(self,itunes_dict):
        self.title = itunes_dict['trackName']
        self.author = itunes_dict['artistName']
        self.itunes_URL = itunes_dict['trackViewUrl']
        self.itunes_id = itunes_dict['trackId']
    def __str__(self):
        return "{} by {}".format(self.title,self.author)
    def __repr__(self):
        return "ITUNES MEDIA: {}".format(self.itunes_id)
    def __len__(self):
        return 0
    def __contains__(self, item):
        return item in self.title
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
        self.boxoffice = soup.find("ul",{"class":"content-meta info"}).find_all("li")[6].find_all("div")[1].text.strip()
    def __str__(self):
        return str(self.name+self.tomato_meter)
    def __repr__(self):
        r = ('Name of Movie: {}\nTomato meter: {}\n'.format(self.name,self.tomato_meter)).encode('utf8', 'replace')
        return r
    def __contains__(self, item):
        return self.name.find(item)
def Cache(url,filename):
    try:
        data = open(filename,'r').read()
    except:
        data = requests.get(url).text
        f = io.open(filename,'w',encoding='utf8')
        f.write(data)
        f.close()
    return data
def Cache_dynamic(url,filename):
    try:
        data = open(filename,'r').read()
    except:
        browser = webdriver.PhantomJS()
        browser.set_window_size(1120,550)
        data = browser.get(url)
        f = io.open(filename,'w',encoding='utf8')
        f.write(data)
        f.close()
    return browser.page_source
testdata = Cache(URL,"movie.html")
# print(testdata)
#div class = critic-score meter, audience-score meter
soup = BeautifulSoup(testdata,'html.parser')
# dyna = Cache_dynamic(big_url,"movies.html")
m_soup = BeautifulSoup(browser.page_source,'html.parser')
url1 = m_soup.find("div",{"class":"mb-movies"}).find_all("div",{"class":"mb-movie"})[0].find("a").get("href")
print(url1)
baseurl = "https://www.rottentomatoes.com"
url_list = []
for i in range(10):
    a = m_soup.find("div",{"class":"mb-movies"}).find_all("div",{"class":"mb-movie"})[i].find("a").get("href")
    url = baseurl+a
    url_list.append(url)
print url_list
movie_list = []
for url in url_list:
    data = Cache(url,url[33:]+".html")
    soup = BeautifulSoup(data,'html.parser')
    movie_list.append(Movie(soup))
print(movie_list)


# all_saints = Movie(soup)
# print(all_saints)
# print(all_saints.tomato_meter)
# print("all" in all_saints)
