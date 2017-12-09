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

insert_into_database()#insert once

def execute_and_print(query, numer_of_results=1):
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    for r in results[:numer_of_results]:
        print(r)
    print('--> Result Rows:', len(results))
    print()
    return results

happy_movies = execute_and_print(""" SELECT "name" FROM "basic_info_of_movie" WHERE "genre" LIKE 'Comedy' """)
print(happy_movies)
a = execute_and_print(""" SELECT ("basic_info_of_movie"."director") FROM "basic_info_of_movie" INNER JOIN "tomato_meter" ON ("tomato_meter"."tomato_meter" = 100) """)
print(a)
