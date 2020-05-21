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
    url_weather = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()
    
    weather_data = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather = requests.get(url_weather.format(lat_param,lng_param)).json()
        
        weather = {
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

        weather_data.append(weather) #add the data for the current city into our list
        
    context = {'weather_data' : weather_data, 'form' : form}  
    return render(request, 'weather_api1/index.html', context) #returns the index.html template
