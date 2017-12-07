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

#havs two csv file: urls, and data
<<<<<<< HEAD
#create 2 tables:
#basic_info_of_movie(name, genre, director, time, boxoffice)
#tomato_meter(name, tomato_meter,tomato_num,audience_score,audience_num)
=======
#create 3 tables: url_of_movie(name, url)
#basic_info_of_movie(name, genre, director, time, boxoffice)
#tomato_meter(name, tomato_meter,tomato_num,audience_score,audience_num)
# Write code / functions to set up database connection and cursor here.
>>>>>>> 370a3f25aeb34ba7953687079c8f525584a7d4de

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

def setup_database():
    # #Table url_of_movie
    # db_cursor.execute("CREATE TABLE url_of_movie(name VARCHAR(128) PRIMARY KEY, url VARCHAR(255))")
    #Table basic_info_of_movie
    try:
        db_cursor.execute("CREATE TABLE basic_info_of_movie(name VARCHAR(128) PRIMARY KEY,genre VARCHAR(128), director VARCHAR(255), time_in_theatre VARCHAR(128), boxoffice VARCHAR(255))")
    except:
        print("table already exists")
    #Table tomato_meter
    try:
        db_cursor.execute("CREATE TABLE tomato_meter(name VARCHAR(128) PRIMARY KEY, tomato_meter VARCHAR(255), tomato_num VARCHAR(255), audience_score VARCHAR(255), audience_num VARCHAR(255))")
    except:
        print("table already exists")

    db_connection.commit()
    print('Setup database complete')
def execute_and_print(query, numer_of_results=1):
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    for r in results[:numer_of_results]:
        print(r)
    print('--> Result Rows:', len(results))
    print()
    return results

#def csv_to_dict_list2(csvfile):
    f = csv.reader(open(csvfile,'r'))
    next(f)
    list_of_dict = []
    for row in f:
        dic = {}
        dic['name'] = row[0]
        dic['tomato_meter'] = row[4]
        dic['tomato_num'] = row[5]
        dic['audience_score'] = row[6]
        dic['audience_num'] = row[7]
    return list_of_dict
db_connection,db_cursor = get_connection_and_cursor()#connect to the database
setup_database()
with open ('data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if "404" not in row[0]:
            print("inputing into the database...")
            db_cursor.execute(
                "INSERT INTO basic_info_of_movie VALUES(%s, %s, %s, %s, %s)", (row[0],row[1],row[2],row[3],row[4])
            )
            db_cursor.execute(
                "INSERT INTO tomato_meter VALUES(%s, %s, %s, %s, %s)", (row[0],row[4],row[5],row[6],row[7])
                )
db_connection.commit()

happy_movies = execute_and_print(""" SELECT "name" FROM "basic_info_of_movie" WHERE "genre" LIKE 'Documentary' """)
print(happy_movies)
