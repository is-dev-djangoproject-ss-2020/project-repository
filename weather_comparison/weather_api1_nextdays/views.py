from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def index(request):
    City.objects.all().delete()
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
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather = requests.get(url_weather.format(lat_param,lng_param)).json()
        
        current_weather = {
            'city' : city,
            'countrycode' : city_countrycode,           
            'utc_time' : datetime.utcfromtimestamp(float(city_weather['current']['dt'])).strftime('%Y-%m-%d %H:%M:%S'),
            'time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'local_time' : datetime.utcfromtimestamp(float(city_weather['current']['dt']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S'),
            'pressure' : city_weather['current']['pressure'],
            'humidity' : city_weather['current']['humidity'],
            'temperature' : city_weather['current']['temp'],
            'description' : city_weather['current']['weather'][0]['description'],
            'icon' : city_weather['current']['weather'][0]['icon'],
        }

        plus1d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,      
            'time' : city_weather['daily'][1]['dt'],
            'pressure' : city_weather['daily'][1]['pressure'],
            'humidity' : city_weather['daily'][1]['humidity'],
            'max_temp' : city_weather['daily'][1]['temp']['max'],
            'min_temp' : city_weather['daily'][1]['temp']['min'],
            'temperature' : city_weather['daily'][1]['temp']['day'],
            'description' : city_weather['daily'][1]['weather'][0]['description'],
            'icon' : city_weather['daily'][1]['weather'][0]['icon'],
        }

        plus2d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,
            'time' : city_weather['daily'][2]['dt'],
            'pressure' : city_weather['daily'][2]['pressure'],
            'humidity' : city_weather['daily'][2]['humidity'],
            'max_temp' : city_weather['daily'][2]['temp']['max'],
            'min_temp' : city_weather['daily'][2]['temp']['min'],
            'temperature' : city_weather['daily'][2]['temp']['day'],
            'description' : city_weather['daily'][2]['weather'][0]['description'],
            'icon' : city_weather['daily'][2]['weather'][0]['icon'],
        }

        plus3d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,
            'time' : city_weather['daily'][3]['dt'],
            'pressure' : city_weather['daily'][3]['pressure'],
            'humidity' : city_weather['daily'][3]['humidity'],
            'max_temp' : city_weather['daily'][3]['temp']['max'],
            'min_temp' : city_weather['daily'][3]['temp']['min'],
            'temperature' : city_weather['daily'][3]['temp']['day'],
            'description' : city_weather['daily'][3]['weather'][0]['description'],
            'icon' : city_weather['daily'][3]['weather'][0]['icon'],
        }

        plus4d_weather = {
            'city' : city,
            'countrycode' : city_countrycode, 
            'time' : city_weather['daily'][4]['dt'],
            'pressure' : city_weather['daily'][4]['pressure'],
            'humidity' : city_weather['daily'][4]['humidity'],
            'max_temp' : city_weather['daily'][4]['temp']['max'],
            'min_temp' : city_weather['daily'][4]['temp']['min'],
            'temperature' : city_weather['daily'][4]['temp']['day'],
            'description' : city_weather['daily'][4]['weather'][0]['description'],
            'icon' : city_weather['daily'][4]['weather'][0]['icon'],
        }
        
        weather_data_current.append(current_weather) #add the data for the current city into our list
        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_current' : weather_data_current, 'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return render(request, 'weather_api1_nextdays/index.html', context) #returns the index.html template
