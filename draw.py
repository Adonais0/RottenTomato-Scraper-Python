# Import statements necessary
import json
import plotly
#-------database-------
from config import *
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import io
import requests
#----------------------
import plotly.plotly as py
from plotly.graph_objs import Scatter,Box, Layout
import plotlyconfig as config_pl

plotly.tools.set_credentials_file(username=config_pl.username, api_key=config_pl.api_key)

#--------------------------------------
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
db_connection,db_cursor = get_connection_and_cursor()

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
