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
#create 2 tables:
#basic_info_of_movie(name, genre, director, time, boxoffice)
#tomato_meter(name, tomato_meter,tomato_num,audience_score,audience_num)


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
