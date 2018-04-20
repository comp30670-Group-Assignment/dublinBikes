from extractorv1 import *
from statsmodels.tools import grouputils
import json

new_conex = Extractor()

output = new_conex.getAverageDailyAvailability()

print(output)


#new_conex.avg_available_bike()

#print(new_conex.avg_available_bike_dict)

#new_conex.avg_available_stand()

#print(new_conex.avg_available_stand_dict)

#print(new_conex.avg_available_bike_dict['BARROW STREET'][0])

#print(new_conex.avg_available_stand_dict['BARROW STREET'][0])



