from flask import Flask, render_template, jsonify
from extractor import extractorv1
import functools
import os
import sqlalchemy as sql
import pandas as pd
import datetime
import pickle
from app import predictions
import time

while True:
    
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    
    if hour == 1 and minute == 1 and second == 1:
    
        predictions("available_bike_stands")
    
        time.sleep((24*60*60) - 1)
