import requests
import json
import time
#import datetime
import mysql.connector
from numbers import Number
import re
from h5py._hl import dataset
from sqlalchemy.sql.expression import except_
import pandas as pd

def regex(input1, input2, input3, input4, input5, input6, input7, input8, input9, input10):

    """This function checks that each JSON element matches the regular expression"""

    # Regular expression pattern
    regEx = "[A-Za-z0-9\/'\,\.\/\-\ ]{1,120}"

    # Regex check
    if re.match(regEx, input1) and re.match(regEx, input2) and re.match(regEx, input3) and re.match(regEx, input4) and re.match(regEx, input5) and re.match(regEx, input6) and re.match(regEx, input7) and re.match(regEx, input8) and re.match(regEx, input9) and re.match(regEx, input10):

        return True

    else:

        return False

def main():

    """Main function that calls the JCDecaux API and writes to database.

    Function retrieves JSON data fromthe JCDecaux API.
    The JSON data is parsed and validated.
    The data is inserted into a remote database."""

    # MySQL connection
    conex = mysql.connector.connect(user='root', password='Rugby_777', database='dublinbikes', host='0.0.0.0')
    
    cursor = conex.cursor()
    
    # JCDecaux API link
    link = "http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=73281f45f2eec1f97e90acdcbacaf4ee"

    # MySQL query
    sqlDelete = "DELETE FROM weatherForecast"
    sqlQuery = "INSERT INTO weatherForecast (dt, temp, humidity, description, pressure, day, hour, icon, dt_txt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    

    # Infinite l
    while True:

        # MySQL object
        
        #cursor.execute(sqlDelete)
        #conex.commit()
        

        # Retrieve and load JSON data
        r = requests.get(link)
        jTxt = json.loads(r.text)

        # If the JSON call was successfuly
        if r.status_code == 200:
            
            for row in jTxt['list']:
                try:
                    
                    hour = pd.to_datetime(row['dt_txt']).hour - 1
                    day = pd.to_datetime(row['dt_txt']).weekday_name
                    print(hour)
                    
                    for i in range(0,3):
                
                        dt = row['dt']
                        temp = row['main']['temp']
                        dt_txt = row['dt_txt']
                        icon = row['weather'][0]['icon']
                        humidity = row['main']['humidity']
                        description = row['weather'][0]['main']
                        pressure = row['main']['pressure']
                        hour += 1
                        
                        
                        args = (int(dt), float(temp), float(humidity), str(description), float(pressure), day, hour, icon, dt_txt)
                        
                        cursor.execute(sqlQuery, args)
                        print("executed")
                        # Commit data to DB
                    
                
                except Exception as e: 
                    print(str(e))
                    pass
                
            conex.commit()
            print("committed")
            # Close MySQL object
            cursor.close()
                
        time.sleep(432000)
                
                
                
if __name__ == "__main__":
    main()
                
                
                
