from flask import Flask, render_template, request, redirect, url_for
import csv
import pyodbc
import pandas as pd
import numpy as np
import os
app = Flask(__name__)

server = 'mysqlserveradb.database.windows.net'
database = 'archana'
username = 'archanat'
password = 'Dheeraj92'

#sql query 
@app.route('/five', methods=['POST'])
def searchmag():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	num = request.form.get("SearchBar")
	cursor.execute("SELECT * FROM [dbo].[qi] WHERE [dbo].[qi].[time2] BETWEEN '7000' AND '8010' AND [dbo].[qi].[net] = 'ci' ")
	row = cursor.fetchall()
	count = len(row)
	cursor.execute("SELECT * FROM [dbo].[qi] WHERE [dbo].[qi].[mag] > '5' ")
	cursor.execute("SELECT TOP 3 * FROM [dbo].[qi] WHERE [dbo].[qi].[mag] > '5' ")
	rows = cursor.fetchall()
	return render_template('five.html', r=rows, c=count)
@app.route('/six', methods=['POST'])
def searchrange():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT * FROM [dbo].[qi] WHERE [dbo].[qi].[latitude] BETWEEN '33.1348333' AND '44.4863333' AND [dbo].[qi].[longitude] BETWEEN '-117.6758333' AND '-64.8555' AND [dbo].[qi].[mag] > '4' ")
	row = cursor.fetchall()
	count = len(row)
	return render_template('six.html', r=row, c=count)
#https://www.geodatasource.com/distance-calculator i used this site to calculate the lat long distances; finding range of places fitting crieteria
@app.route('/latlong', methods=['POST'])
def searchlatlong():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT [dbo].[all_month].[place] FROM [dbo].[all_month] where [dbo].[all_month].[latitude] BETWEEN '60.891' AND '61.30' AND [dbo].[all_month].[longitude] BETWEEN '-150.3505' AND '-150' ")
	row = cursor.fetchall()
	return render_template('latlongdist.html', r=row)
#finding if large earth quakes happen during day or night
@app.route('/dayornight', methods=['POST'])
def searchdayornight():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
#all earthquakes between 10PM and 5AM to see how many occured at night	
	cursor.execute("SELECT [dbo].[all_month].[time], [dbo].[all_month].[mag], [dbo].[all_month].[place] FROM [all_month] WHERE [dbo].[all_month].[mag] > '4' AND (DATEADD(day, -DATEDIFF(day, 0, time), time) > '00:10:10.000' and DATEADD(day, -DATEDIFF(day, 0, time), time) < '05:00:00.000') ")
	row = cursor.fetchall()
	count = len(row)
	rem = 12052
	return render_template('dayornight.html', c=count, b=rem)
#clustering by counting mag of different numbers
@app.route('/cluster', methods=['POST'])
def cluster():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '0.0' AND '1.0' ")
	row = cursor.fetchall()
	a = len(row)
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '1.0' AND '2.0' ")
	row = cursor.fetchall()
	b = len(row)
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '2.0' AND '3.0' ")
	row = cursor.fetchall()
	c = len(row)
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '3.0' AND '4.0' ")
	row = cursor.fetchall()
	d = len(row)
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '4.0' AND '5.0' ")
	row = cursor.fetchall()
	e = len(row)
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '5.0' AND '6.0' ")
	row = cursor.fetchall()
	f = len(row)
	cursor.execute("SELECT * FROM [dbo].[all_month] WHERE [dbo].[all_month].[mag] BETWEEN '6.0' AND '7.0' ")
	row = cursor.fetchall()
	g = len(row)
	return render_template('cluster.html', r=row, a=a, b=b, c=c, d=d, e=e, f=f, g=g)	
@app.route('/')
def hello():
	return render_template('home.html')
