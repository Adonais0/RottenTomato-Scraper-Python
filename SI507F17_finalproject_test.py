import unittest
import csv
from SI507F17_finalproject import *
from draw import *
import json
import plotly
from config import *
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import io
import requests

class Cache(unittest.TestCase):#1 tests
    def setUp(self):
        self.url = open("url.csv")
        self.data = open("data.csv")
        self.js = open("cache_contents.json")

    def test_files_exist(self):
        self.assertTrue(self.url.read())
        self.assertTrue(self.data.read())
        self.assertTrue(self.js.read())

    def tearDown(self):
        self.url.close()
        self.data.close()
        self.js.close()

class TestMovie(unittest.TestCase):#5 tests
    def setUp(self):
        self.url = 'https://www.rottentomatoes.com/m/keplers_dream'
        self.data = CACHE_DICTION[self.url]#return html
        self.soup_movie_inst = BeautifulSoup(self.data, 'html.parser')
        self.sample_inst = Movie(self.soup_movie_inst)

    def test_soup_inst(self):
        self.assertTrue(self.soup_movie_inst.find("h1"))
        self.assertTrue(self.soup_movie_inst.find("ul",{"class":"content-meta info"}).find_all("li")[1].find("a"))
        self.assertTrue(self.soup_movie_inst.find("ul",{"class":"content-meta info"}).find_all("li")[4].find_all("div")[1])
        self.assertTrue(self.soup_movie_inst.find("div",{"class":"critic-score meter"}).find("span", {"class": "superPageFontColor"}).find("span").text)

    def test_movie_constructor(self):
        self.assertIsInstance(self.sample_inst.name,str)
        self.assertIsInstance(self.sample_inst.genre, str)
        self.assertIsInstance(self.sample_inst.director, str)
        self.assertIsInstance(self.sample_inst.date, str)
        self.assertIsInstance(self.sample_inst.tomato_meter, int)
        self.assertIsInstance(self.sample_inst.tomato_num, int)
        self.assertIsInstance(self.sample_inst.audience_num, (int))

    def test_movie_string(self):
        self.assertEqual(self.sample_inst.__str__(),"\nMovie Name: Kepler's Dream (2017)\n Meter: 50")
    def test_movie_repr(self):
        self.assertEqual(self.sample_inst.__repr__(),"\nMovie Name: Kepler's Dream (2017)")
    def test_movie_contain(self):
        self.assertTrue("le" in self.sample_inst)
        self.assertTrue("50" in self.sample_inst)

class MovieList(unittest.TestCase): #2 tests
    def setUp(self):
        pass
    def test_list_movies(self):
        self.assertIsInstance(movie_list,list)
    def test_list_elem_types(self):
        print(type(movie_list[1]))
        self.assertIsInstance(movie_list[1],Movie)

class TestDataCsv(unittest.TestCase):#2 tests
    def setUp(self):#test csv file
        with open('data.csv') as self.f:
            self.first_colum = []#a row is a list of data of a single movie
            self.readCSV = list(csv.reader(self.f, delimiter = ','))
            self.first_row = self.readCSV[1]
            for row in self.readCSV:
                self.first_colum.append(row[0])

    def test_basic_data(self):
        self.assertEqual(self.first_row[1],'Animation')
        self.assertEqual(self.first_row[2],'Kyle Balda')
        self.assertTrue("spi" in self.first_row[0])

    def test_tomato_meter(self):
        self.assertEqual(self.first_row[-5].strip(),'60')
        self.assertIsInstance(self.first_row[-2],str)

class TestDatabase(unittest.TestCase):#3 tests
    def setUp(self):
        self.a = db_cursor.execute(""" SELECT * FROM "basic_info_of_movie" INNER JOIN "tomato_meter" ON "basic_info_of_movie"."name" = "tomato_meter"."name" """)
        self.data = db_cursor.fetchall()
        self.genre_list = []
        for d in self.data:
            self.genre_list.append(d['genre'])
        self.c = open('config.py','r')

    def test_conf(self):
        self.assertTrue(self.c.read())

    def test_db(self):
        self.assertIsInstance(self.data[0]['name'], str)
        self.assertIsInstance(self.data[0]['genre'], str)
        self.assertIsInstance(self.data[0]['movie_id'], int)
        self.assertIsInstance(self.data[0]['tomato_meter'], int)

    def test_genre_list(self):
        self.assertIsInstance(self.genre_list[0],str)
        self.assertEqual(self.genre_list[0],'Animation')

    def tearDown(self):
        self.c.close()

class TestPlotly(unittest.TestCase):# 3 test

    def setUp(self):
        self.con = open('plotlyconfig.py')
        self.show = show1()

    def test_config(self):
        self.assertTrue(self.con.read())

    def test_show(self):
        self.assertTrue(self.show)

    def tearDown(self):
        self.con.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
