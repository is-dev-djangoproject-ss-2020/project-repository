from django.shortcuts import render
from django.contrib import messages
import math
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .calendar_tool import calendar_values
from .calendar_tool import date_converter
import re

def openweathermap_forecast(request):
    #City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = []
    weather_data_plus1d = []
    weather_data_plus2d = []
    weather_data_plus3d = []
    weather_data_plus4d = []
    calendar_data = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather = requests.get(url_weather.format(lat_param,lng_param)).json()

        plus1d_weather = {
            'openweathermap_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'openweathermap_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'openweathermap_city_1' : city,
            'openweathermap_provider_1' : 'OpenWeatherMap',
            'openweathermap_countrycode_1' : city_countrycode,      
            'openweathermap_time_1' : city_weather['daily'][1]['dt'],
            'openweathermap_pressure_1' : city_weather['daily'][1]['pressure'],
            'openweathermap_humidity_1' : city_weather['daily'][1]['humidity'],
            'openweathermap_max_temp_1' : city_weather['daily'][1]['temp']['max'],
            'openweathermap_min_temp_1' : city_weather['daily'][1]['temp']['min'],
            'openweathermap_temperature_1' : city_weather['daily'][1]['temp']['day'],
            'openweathermap_description_1' : city_weather['daily'][1]['weather'][0]['description'],
            'openweathermap_icon_1' : city_weather['daily'][1]['weather'][0]['icon'],
            'openweathermap_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'openweathermap_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'openweathermap_city_2' : city,
            'openweathermap_provider_2' : 'OpenWeatherMap',
            'openweathermap_countrycode_2' : city_countrycode,
            'openweathermap_time_2' : city_weather['daily'][2]['dt'],
            'openweathermap_pressure_2' : city_weather['daily'][2]['pressure'],
            'openweathermap_humidity_2' : city_weather['daily'][2]['humidity'],
            'openweathermap_max_temp_2' : city_weather['daily'][2]['temp']['max'],
            'openweathermap_min_temp_2' : city_weather['daily'][2]['temp']['min'],
            'openweathermap_temperature_2' : city_weather['daily'][2]['temp']['day'],
            'openweathermap_description_2' : city_weather['daily'][2]['weather'][0]['description'],
            'openweathermap_icon_2' : city_weather['daily'][2]['weather'][0]['icon'],
            'openweathermap_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'openweathermap_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'openweathermap_city_3' : city,
            'openweathermap_provider_3' : 'OpenWeatherMap',
            'openweathermap_countrycode_3' : city_countrycode,
            'openweathermap_time_3' : city_weather['daily'][3]['dt'],
            'openweathermap_pressure_3' : city_weather['daily'][3]['pressure'],
            'openweathermap_humidity_3' : city_weather['daily'][3]['humidity'],
            'openweathermap_max_temp_3' : city_weather['daily'][3]['temp']['max'],
            'openweathermap_min_temp_3' : city_weather['daily'][3]['temp']['min'],
            'openweathermap_temperature_3' : city_weather['daily'][3]['temp']['day'],
            'openweathermap_description_3' : city_weather['daily'][3]['weather'][0]['description'],
            'openweathermap_icon_3' : city_weather['daily'][3]['weather'][0]['icon'],
            'openweathermap_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'openweathermap_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'openweathermap_city_4' : city,
            'openweathermap_provider_4' : 'OpenWeatherMap',
            'openweathermap_countrycode_4' : city_countrycode,
            'openweathermap_time_4' : city_weather['daily'][4]['dt'],
            'openweathermap_pressure_4' : city_weather['daily'][4]['pressure'],
            'openweathermap_humidity_4' : city_weather['daily'][4]['humidity'],
            'openweathermap_max_temp_4' : city_weather['daily'][4]['temp']['max'],
            'openweathermap_min_temp_4' : city_weather['daily'][4]['temp']['min'],
            'openweathermap_temperature_4' : city_weather['daily'][4]['temp']['day'],
            'openweathermap_description_4' : city_weather['daily'][4]['weather'][0]['description'],
            'openweathermap_icon_4' : city_weather['daily'][4]['weather'][0]['icon'],
        }

        weather_data_plus1d.append(plus1d_weather)


    calendar = {
        'day_1' : date_converter(1),
        'day_2' : date_converter(2),
        'day_3' : date_converter(3),
        'day_4' : date_converter(4),
    }
    calendar_data.append(calendar)

            
    context = {'calendar_data' : calendar_data, 'weather_data_plus1d' : weather_data_plus1d, 'form' : form}  
    return context

###################
