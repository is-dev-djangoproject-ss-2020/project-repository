import shutil
import json
import time
import os

from django.shortcuts import render
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .calendar_tool import calendar_values
from .calendar_tool import date_converter
import re

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.' + directory)

def weatherbit_processing(request):
    #City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_1 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_2 = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    url_weather_3 = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=forecast_7days_simple&latitude={}&longitude={}'
    url_weather_4 = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    data = {}
    data['tomorrow'] = []
    data['in_2_days'] = []
    data['in_3_days'] = []
    data['in_4_days'] = []

    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_1 = requests.get(url_weather_1.format(lat_param,lng_param)).json()
        city_weather_2 = requests.get(url_weather_2.format(lat_param,lng_param)).json()
        city_weather_3 = requests.get(url_weather_3.format(lat_param,lng_param)).json()
        city_weather_4 = requests.get(url_weather_4.format(lat_param,lng_param)).json()

        icon_link_forecast_1=city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['iconLink']
        if icon_link_forecast_1 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_1 = 3
        else:
            icon_code_forecast_1=int(''.join(filter(str.isdigit, icon_link_forecast_1)))

        icon_link_forecast_2=city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['iconLink']
        if icon_link_forecast_2 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_2 = 3
        else:
            icon_code_forecast_2=int(''.join(filter(str.isdigit, icon_link_forecast_2)))

        icon_link_forecast_3=city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['iconLink']
        if icon_link_forecast_3 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_3 = 3
        else:
            icon_code_forecast_3=int(''.join(filter(str.isdigit, icon_link_forecast_3)))

        icon_link_forecast_4=city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['iconLink']
        if icon_link_forecast_4 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_4 = 3
        else:
            icon_code_forecast_4=int(''.join(filter(str.isdigit, icon_link_forecast_4)))

        data = {}
        data['tomorrow'] = []
        data['in_2_days'] = []
        data['in_3_days'] = []
        data['in_4_days'] = []

        data['tomorrow'].append({
            'weatherbit_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'weatherbit_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'weatherbit_city_1' : str(city.name),
            'weatherbit_countrycode_1' : city_countrycode,      
            'weatherbit_time_1' : city_weather_2['data'][1]['ts'],
            'weatherbit_pressure_1' : city_weather_2['data'][1]['pres'],
            'weatherbit_humidity_1' : city_weather_2['data'][1]['rh'],
            'weatherbit_max_temp_1' : city_weather_2['data'][1]['max_temp'],
            'weatherbit_min_temp_1' : city_weather_2['data'][1]['min_temp'],
            'weatherbit_temperature_1' : city_weather_2['data'][1]['temp'],
            'weatherbit_description_1' : city_weather_2['data'][1]['weather']['description'],
            'weatherbit_provider_1' : 'Weatherbit',
        })

        data['in_2_days'].append({
            'weatherbit_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'weatherbit_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'weatherbit_city_2' : str(city.name),
            'weatherbit_countrycode_2' : city_countrycode,      
            'weatherbit_time_2' : city_weather_2['data'][2]['ts'],
            'weatherbit_pressure_2' : city_weather_2['data'][2]['pres'],
            'weatherbit_humidity_2' : city_weather_2['data'][2]['rh'],
            'weatherbit_max_temp_2' : city_weather_2['data'][2]['max_temp'],
            'weatherbit_min_temp_2' : city_weather_2['data'][2]['min_temp'],
            'weatherbit_temperature_2' : city_weather_2['data'][2]['temp'],
            'weatherbit_description_2' : city_weather_2['data'][2]['weather']['description'],
            'weatherbit_provider_2' : 'Weatherbit',    
        })

        data['in_3_days'].append({
            'weatherbit_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'weatherbit_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'weatherbit_city_3' : str(city.name),
            'weatherbit_countrycode_3' : city_countrycode,      
            'weatherbit_time_3' : city_weather_2['data'][3]['ts'],
            'weatherbit_pressure_3' : city_weather_2['data'][3]['pres'],
            'weatherbit_humidity_3' : city_weather_2['data'][3]['rh'],
            'weatherbit_max_temp_3' : city_weather_2['data'][3]['max_temp'],
            'weatherbit_min_temp_3' : city_weather_2['data'][3]['min_temp'],
            'weatherbit_temperature_3' : city_weather_2['data'][3]['temp'],
            'weatherbit_description_3' : city_weather_2['data'][3]['weather']['description'],
            'weatherbit_provider_3' : 'Weatherbit',    
        })

        data['in_4_days'].append({
            'weatherbit_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'weatherbit_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'weatherbit_city_4' : str(city.name),
            'weatherbit_countrycode_4' : city_countrycode,      
            'weatherbit_time_4' : city_weather_2['data'][4]['ts'],
            'weatherbit_pressure_4' : city_weather_2['data'][4]['pres'],
            'weatherbit_humidity_4' : city_weather_2['data'][4]['rh'],
            'weatherbit_max_temp_4' : city_weather_2['data'][4]['max_temp'],
            'weatherbit_min_temp_4' : city_weather_2['data'][4]['min_temp'],
            'weatherbit_temperature_4' : city_weather_2['data'][4]['temp'],
            'weatherbit_description_4' : city_weather_2['data'][4]['weather']['description'],
            'weatherbit_provider_4' : 'Weatherbit',    
        })

    unix_time = int(time.time())
    folder_name = 'forecasts_' + str(unix_time)
    file_name = folder_name + '/' + str(unix_time) + '_forecast.txt'
    createFolder('./' + folder_name + '/')
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

    source = os.getcwd() + '/' + folder_name
    name = input("Provide the path to which your forecast should be saved!")
    destination = name
    dest = shutil.move(source, destination)

    message_dict = {'message' : 'Your report was generated', 'message2' : 'Now use the two buttons below to continue'}
    context = {'message_dict' : message_dict, 'form' : form}
    return context
