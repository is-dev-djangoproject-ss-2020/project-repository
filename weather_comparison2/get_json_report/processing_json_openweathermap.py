import shutil
import json
import time
import os
import requests
import math
import re

from django.shortcuts import render
from django.contrib import messages
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .calendar_tool import calendar_values
from .calendar_tool import date_converter

def createFolder(directory):
    """If the web service is locally installed, this function should create a folder at the user's request."""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.' + directory)

def openweathermap_processing(request):
    """Retrieves the weather data and generates a JSON report based on OpenWeatherMap."""
    #City.objects.all().delete() #(uncomment to allow the use of various cities simultaneously)
    cities = City.objects.all() #return all the cities in the database
    url_weather_1 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    #url_weather_2 = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    #url_weather_3 = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=forecast_7days_simple&latitude={}&longitude={}'
    #url_weather_4 = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    data = {} #sets up the necessary places for the JSON values (filled with variables later on)
    data['tomorrow'] = []
    data['in_2_days'] = []
    data['in_3_days'] = []
    data['in_4_days'] = []
        
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0: #if no results are found, the loop's execution should be stopped and we get an empty report
            messages.error(request, "Error")
            break
        
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_1 = requests.get(url_weather_1.format(lat_param,lng_param)).json() #specification of the URL for OpenWeatherMap

        data['tomorrow'].append({
            'openweathermap_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'openweathermap_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'openweathermap_city_1' : str(city.name),
            'openweathermap_countrycode_1' : city_countrycode,      
            'openweathermap_time_1' : city_weather_1['daily'][1]['dt'],
            'openweathermap_pressure_1' : city_weather_1['daily'][1]['pressure'],
            'openweathermap_humidity_1' : city_weather_1['daily'][1]['humidity'],
            'openweathermap_max_temp_1' : city_weather_1['daily'][1]['temp']['max'],
            'openweathermap_min_temp_1' : city_weather_1['daily'][1]['temp']['min'],
            'openweathermap_temperature_1' : city_weather_1['daily'][1]['temp']['day'],
            'openweathermap_description_1' : city_weather_1['daily'][1]['weather'][0]['description'],
            'openweathermap_provider_1' : 'OpenWeatherMap',
        })

        data['in_2_days'].append({
            'openweathermap_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'openweathermap_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'openweathermap_city_2' : str(city.name),
            'openweathermap_countrycode_2' : city_countrycode,
            'openweathermap_time_2' : city_weather_1['daily'][2]['dt'],
            'openweathermap_pressure_2' : city_weather_1['daily'][2]['pressure'],
            'openweathermap_humidity_2' : city_weather_1['daily'][2]['humidity'],
            'openweathermap_max_temp_2' : city_weather_1['daily'][2]['temp']['max'],
            'openweathermap_min_temp_2' : city_weather_1['daily'][2]['temp']['min'],
            'openweathermap_temperature_2' : city_weather_1['daily'][2]['temp']['day'],
            'openweathermap_description_2' : city_weather_1['daily'][2]['weather'][0]['description'],
            'openweathermap_provider_2' : 'OpenWeatherMap',
        })

        data['in_3_days'].append({
            'openweathermap_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'openweathermap_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'openweathermap_city_3' : str(city.name),
            'openweathermap_countrycode_3' : city_countrycode,
            'openweathermap_time_3' : city_weather_1['daily'][3]['dt'],
            'openweathermap_pressure_3' : city_weather_1['daily'][3]['pressure'],
            'openweathermap_humidity_3' : city_weather_1['daily'][3]['humidity'],
            'openweathermap_max_temp_3' : city_weather_1['daily'][3]['temp']['max'],
            'openweathermap_min_temp_3' : city_weather_1['daily'][3]['temp']['min'],
            'openweathermap_temperature_3' : city_weather_1['daily'][3]['temp']['day'],
            'openweathermap_description_3' : city_weather_1['daily'][3]['weather'][0]['description'],
            'openweathermap_provider_3' : 'OpenWeatherMap',
        })

        data['in_4_days'].append({
            'openweathermap_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'openweathermap_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'openweathermap_city_4' : str(city.name),
            'openweathermap_countrycode_4' : city_countrycode,
            'openweathermap_time_4' : city_weather_1['daily'][4]['dt'],
            'openweathermap_pressure_4' : city_weather_1['daily'][4]['pressure'],
            'openweathermap_humidity_4' : city_weather_1['daily'][4]['humidity'],
            'openweathermap_max_temp_4' : city_weather_1['daily'][4]['temp']['max'],
            'openweathermap_min_temp_4' : city_weather_1['daily'][4]['temp']['min'],
            'openweathermap_temperature_4' : city_weather_1['daily'][4]['temp']['day'],
            'openweathermap_description_4' : city_weather_1['daily'][4]['weather'][0]['description'],
            'openweathermap_provider_4' : 'OpenWeatherMap',
        })

    unix_time = int(time.time()) #get unix time in seconds as an integer
    folder_name = 'forecasts_' + str(unix_time) #use unix time as a part of the folder name (to avoid ambiguities)
    file_name = folder_name + '/' + str(unix_time) + '_forecast.txt' #specification of a file name (again with unix time)
    createFolder('./' + folder_name + '/') #create folder with the specified folder name (see the function above)
    with open(file_name, 'w') as outfile: #created JSON report is saved to a newly generated file with the new filename
        json.dump(data, outfile)

    source = os.getcwd() + '/' + folder_name #take the newly created folder as an object to move ...
    name = input("Provide the path to which your forecast should be saved!") # ... to a place that the user specifies with the input function
    destination = name
    dest = shutil.move(source, destination) #moves the folder to the new destination

    message_dict = {'message' : 'Your report was generated', 'message2' : 'Now use the two buttons below to continue'} #response messages (shortcoming: they are also shown if the report is empty)
    context = {'message_dict' : message_dict, 'form' : form}
    return context
