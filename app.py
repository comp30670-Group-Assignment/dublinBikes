"""
Authors:
Hugh O'Brien
Tim Madigan
Aalasa Fidler
"""
from flask import Flask, render_template, jsonify
from extractor import extractorv1
import functools
import os
import sqlalchemy as sql
import pandas as pd
import datetime
import json
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Binary
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract
import datetime
import sqlalchemy as sql
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.externals import joblib
"""
import pickle


def predictions(bike):
	
	if bike == "available_bikes":
		b = "bikes"
	else:
		b = "stands"
		
	conex = sql.create_engine("mysql+pymysql://root:Rugby_777@localhost/dublinbikes")
	
	now = datetime.datetime.now()
	        
	day = now.day
	
	
	#pull today's forecast
	
	
	
	
	#for each station...
	
	for a in range(1,103):
		
		
		predictions = {}
		
		try:
			
			

			predictions[a] = []
			
			#pull average bike data for that station aswell as weather forecast
			
			df_weather = pd.read_sql_query("SELECT temp, humidity, pressure, hour, dt_txt, description from weatherForecast where DAY(dt_txt) = %d" % day, conex)
			
			df_bikes_test = pd.read_sql_query("SELECT AVG(%s) as %s, HOUR(timestamp) as hour from data where number = %d group by hour" % (bike, bike, a), conex)
			
			
			for j, row in df_weather.iterrows():
	
			    df_weather.loc[j, 'day'] = pd.to_datetime(row['dt_txt']).weekday_name
			
			#make dummy variables for each day of the week
			dummy = pd.get_dummies(df_weather['day'])
			df_weather = pd.concat([dummy, df_weather], axis = 1)
			days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
			for x in days:
			    if df_weather['day'][0] != x:
			
			        df_weather[x] = [0] * len(df_weather)
			
			
			
			#construct weather dummy variables by getting all unique weather descriptions from the database
			dummy = pd.get_dummies(df_weather['description'])
			df_weather = pd.concat([df_weather,dummy], axis = 1) 
			unique_weather = pd.read_sql_query("SELECT DISTINCT(main) FROM dublin_weather", conex)
			for y, row2 in unique_weather.iterrows():
			
			    if not row2['main'] in df_weather['description'].values:
			
			        df_weather[row2['main']] = [0] * len(df_weather)
			        
			df_weather = df_weather.drop(['day','description','dt_txt'], axis = 1)
			
			df_weather = df_weather[['Friday','Saturday','Sunday','Thursday','Tuesday','Wednesday','temp','pressure','humidity','hour','Monday','Clear','Clouds','Drizzle','Mist','Rain','Snow','Fog']]
			
			
			rf_test = pickle.load(open("static/pickle/%s_%d.pkl" % (b, a), 'rb'))
			
			prediction = rf_test.predict(df_weather.values)
			
			prediction = prediction.tolist()
			
			predictions[a] = prediction
		
		except:
			print(a)
			predictions[a] = []
			predictions[a] = [0] * 24
			pass
		
		fh = open("static/predictions/%s.json" % a, 'w')
		fh.write(json.dumps(predictions))

	
	

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('home.html', x=os.path.join(app.instance_path));

@app.route('/_map_data')
def add_numbers():
	recent = extractorv1.Extractor();
	return jsonify(recent.getRecent());


@app.route('/_weather')
def weather():
	weather = extractorv1.Extractor();
	return jsonify(weather.getWeather())

@app.route('/_predictions/<int:file_id>')
def prediction_data(file_id):
	predictionList = [];
	filePred = "static/predictions/%s.json" % file_id
	fileOpen  = open(filePred, "r");
	for line in fileOpen:
		predictionList.append(line);
	return jsonify(predictionList);

@app.route('/_trends')
def bike_trends():
	trends = extractorv1.Extractor();
	return jsonify(trends.getAverageDailyAvailability())

@functools.lru_cache(maxsize=256)
@app.route('/_drop_data')
def dropdown():
	stations = extractorv1.Extractor();
	return jsonify(stations.stationNames());

if __name__ == '__main__':
	app.run(debug=True)