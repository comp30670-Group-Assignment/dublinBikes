import requests
import json
import time
#import datetime
import mysql.connector
from numbers import Number
import re
from h5py._hl import dataset

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
	link = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&&apiKey=4dc48c410fefd7a42d52cdc4a9c6eb7ce0f67ae0"

	# MySQL query
	sqlQuery = "INSERT INTO data (data_set_id, data_id, number, name, address, position_lat, position_lng, bike_stands, status, available_bike_stands, available_bikes, last_update)" \
	"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	
	dataset_query = "SELECT MAX(data_set_id) FROM data"
	
	cursor.execute(dataset_query)

	# Set ID value for each time a fresh set of JSON data is pulled from the API
	dataSet = cursor.fetchall()[0][0] + 1

	# Infinite loop
	while True:

		# MySQL object
		

		# Retrieve and load JSON data
		r = requests.get(link)
		jTxt = json.loads(r.text)

		# If the JSON call was successfuly
		if r.status_code == 200:

			#try:

				# For every row of JSON elements
			count = 0
			for row in jTxt:
				

				# Pass JSON elements through number and string validators
				if isinstance(jTxt[count]['number'], Number) == True and isinstance(jTxt[count]['name'], str) == True and isinstance(jTxt[count]['address'], str) == True and isinstance(jTxt[count]['position']['lat'], Number) == True and isinstance(jTxt[count]['position']['lng'], Number) == True and isinstance(jTxt[count]['bike_stands'], Number) == True and isinstance(jTxt[count]['status'], str) == True and isinstance(jTxt[count]['available_bike_stands'], Number) == True and isinstance(jTxt[count]['available_bikes'], Number) == True and isinstance(jTxt[count]['last_update'], Number):		

					# Pass JSON elements through a regular expression check
					if regex(str(jTxt[count]['number']), str(jTxt[count]['name']), str(jTxt[count]['address']), str(jTxt[count]['position']['lat']), str(jTxt[count]['position']['lng']), str(jTxt[count]['bike_stands']), str(jTxt[count]['status']), str(jTxt[count]['available_bike_stands']), str(jTxt[count]['available_bikes']), str(jTxt[count]['last_update'])) == True:

						# MySQL arguments
						args = (int(dataSet), int(count), int(jTxt[count]['number']), str(jTxt[count]['name']), str(jTxt[count]['address']), float(jTxt[count]['position']['lat']), float(jTxt[count]['position']['lng']), int(jTxt[count]['bike_stands']), str(jTxt[count]['status']), int(jTxt[count]['available_bike_stands']), int(jTxt[count]['available_bikes']), int(jTxt[count]['last_update']))

						# Execute query
						cursor.execute(sqlQuery, args)

					else:
						# Error occured so continue FOR loop
						continue
				else:

					# Error occured so continue FOR loop
					continue

				# Increase counter variable for iterating over JSON data
				count += 1

			#except:
				#print("except")
				# Error occured so rollback
				#conex.rollback()

			#finally:

				# Commit data to DB
			conex.commit()
			# Close MySQL object
			cursor.close()

		# Increment data set counter
		dataSet += 1

		# Sleep for 5 minutes before calling API again
		time.sleep(300)

	# Close connection
	conex.close()

if __name__ == '__main__':
	main()
