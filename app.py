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
@app.route('/seven', methods=['POST'])
def searchlatlong():
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT * FROM [dbo].[qi] WHERE [dbo].[qi].[time2] BETWEEN '7200' AND '7800' AND [dbo].[qi].[net] = 'nc' AND [dbo].[qi].[mag] > '2' ")
	row = cursor.fetchall()
	count = len(row)
	return render_template('seven.html', r=row, c=count)

@app.route('/')
def hello():
	return render_template('home.html')
