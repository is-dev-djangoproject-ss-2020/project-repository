import shutil
import json
import time
import os

from django.shortcuts import render
from django.contrib import messages
import requests
import math
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

def allforecasts_processing(request):
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

        data['tomorrow'].append({
            'here_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'here_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'here_city_1' : str(city.name),
            'here_countrycode_1' : city_countrycode,      
            'here_time_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['utcTime'],
            'here_pressure_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['barometerPressure'],
            'here_humidity_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['humidity'],
            'here_max_temp_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'],
            'here_min_temp_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['lowTemperature'],
            'here_temperature_1' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['description'],
            'here_provider_1' : 'here.com',
        })

        data['in_2_days'].append({
            'here_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'here_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'here_city_2' : str(city.name),
            'here_countrycode_2' : city_countrycode,      
            'here_time_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['utcTime'],
            'here_pressure_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['barometerPressure'],
            'here_humidity_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['humidity'],
            'here_max_temp_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['highTemperature'],
            'here_min_temp_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['lowTemperature'],
            'here_temperature_2' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['description'],
            'here_provider_2' : 'here.com',    
        })

        data['in_3_days'].append({
            'here_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'here_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'here_city_3' : str(city.name),
            'here_countrycode_3' : city_countrycode,      
            'here_time_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['utcTime'],
            'here_pressure_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['barometerPressure'],
            'here_humidity_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['humidity'],
            'here_max_temp_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['highTemperature'],
            'here_min_temp_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['lowTemperature'],
            'here_temperature_3' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['description'],
            'here_provider_3' : 'here.com',    
        })

        data['in_4_days'].append({
            'here_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'here_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'here_city_4' : str(city.name),
            'here_countrycode_4' : city_countrycode,      
            'here_time_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['utcTime'],
            'here_pressure_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['barometerPressure'],
            'here_humidity_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['humidity'],
            'here_max_temp_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['highTemperature'],
            'here_min_temp_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['lowTemperature'],
            'here_temperature_4' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['description'],
            'here_provider_4' : 'here.com',    
        })
        
        data['tomorrow'].append({
            'worldweatheronline_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'worldweatheronline_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'worldweatheronline_city_1' : str(city.name),
            'worldweatheronline_countrycode_1' : city_countrycode,      
            'worldweatheronline_time_1' : city_weather_4["data"]["weather"][1]["date"],
            'worldweatheronline_pressure_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_1' : city_weather_4["data"]["weather"][1]["maxtempC"],
            'worldweatheronline_min_temp_1' : city_weather_4["data"]["weather"][1]["mintempC"],
            'worldweatheronline_temperature_1' : math.ceil(float(city_weather_4["data"]["weather"][1]["maxtempC"])/2+float(city_weather_4["data"]["weather"][1]["mintempC"])/2),
            'worldweatheronline_description_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_provider_1' : 'WorldWeatherOnline',
        })

        data['in_2_days'].append({
            'worldweatheronline_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'worldweatheronline_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'worldweatheronline_city_2' : str(city.name),
            'worldweatheronline_countrycode_2' : city_countrycode,      
            'worldweatheronline_time_2' : city_weather_4["data"]["weather"][2]["date"],
            'worldweatheronline_pressure_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_2' : city_weather_4["data"]["weather"][2]["maxtempC"],
            'worldweatheronline_min_temp_2' : city_weather_4["data"]["weather"][2]["mintempC"],
            'worldweatheronline_temperature_2' : math.ceil(float(city_weather_4["data"]["weather"][2]["maxtempC"])/2+float(city_weather_4["data"]["weather"][2]["mintempC"])/2),
            'worldweatheronline_description_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_provider_2' : 'WorldWeatherOnline',    
        })

        data['in_3_days'].append({
            'worldweatheronline_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'worldweatheronline_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'worldweatheronline_city_3' : str(city.name), 
            'worldweatheronline_countrycode_3' : city_countrycode,      
            'worldweatheronline_time_3' : city_weather_4["data"]["weather"][3]["date"],
            'worldweatheronline_pressure_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_3' : city_weather_4["data"]["weather"][3]["maxtempC"],
            'worldweatheronline_min_temp_3' : city_weather_4["data"]["weather"][3]["mintempC"],
            'worldweatheronline_temperature_3' : math.ceil(float(city_weather_4["data"]["weather"][3]["maxtempC"])/2+float(city_weather_4["data"]["weather"][3]["mintempC"])/2),
            'worldweatheronline_description_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_provider_3' : 'WorldWeatherOnline',    
        })

        data['in_4_days'].append({
            'worldweatheronline_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'worldweatheronline_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'worldweatheronline_city_4' : str(city.name),   
            'worldweatheronline_countrycode_4' : city_countrycode,             'worldweatheronline_countrycode_4' : city_countrycode,      
            'worldweatheronline_time_4' : city_weather_4["data"]["weather"][4]["date"],
            'worldweatheronline_pressure_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_4' : city_weather_4["data"]["weather"][4]["maxtempC"],
            'worldweatheronline_min_temp_4' : city_weather_4["data"]["weather"][4]["mintempC"],
            'worldweatheronline_temperature_4' : math.ceil(float(city_weather_4["data"]["weather"][4]["maxtempC"])/2+float(city_weather_4["data"]["weather"][4]["mintempC"])/2),
            'worldweatheronline_description_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_provider_4' : 'WorldWeatherOnline',    
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
