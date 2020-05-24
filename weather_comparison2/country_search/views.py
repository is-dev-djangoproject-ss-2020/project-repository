from django.shortcuts import render
from django.contrib import messages
import math
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .calendar_tool import date_converter
from .calendar_tool import calendar_values
import re

def index(request):
    City.objects.all().delete() #(uncommented to allow the use of one city at a time only)
    cities = City.objects.all() #return all the cities in the database
    url_country = 'https://restcountries.eu/rest/v2/name/{}'
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    #url_weather_current = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=observation&latitude={}&longitude={}'
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
        capital_request = requests.get(url_country.format(city)).json()
        #if capital_request["message"] == "Not found":
        #    messages.error(request, "Error")
        #    break
        capital_name = capital_request[0]["capital"]
        city_geodata = requests.get(url_geodata.format(capital_name)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        #city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json()
     #   city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json()

        current_weather = {
            'weekday' : calendar_values()['calendar_data'][0]['weekday_today'],
            'date' : calendar_values()['calendar_data'][0]['date_object_today'],
            'city' : capital_name,       
            'utc_time' : city_weather_forecast["data"]["current_condition"][0]["observation_time"],
            'time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'local_time' : city_weather_forecast["data"]["current_condition"][0]["localObsDateTime"],
            'pressure' : city_weather_forecast["data"]["current_condition"][0]["pressure"],
            'humidity' : city_weather_forecast["data"]["current_condition"][0]["humidity"],
            'temperature' : city_weather_forecast["data"]["current_condition"][0]["temp_C"],
            'description' : city_weather_forecast["data"]["current_condition"][0]["weatherDesc"][0]["value"],
            'icon' : city_weather_forecast["data"]["current_condition"][0]["weatherIconUrl"][0]["value"],
        }

        plus1d_weather = {
            'weekday' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'date' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'city' : capital_name,     
            'time' : city_weather_forecast["data"]["weather"][1]["date"],
            'pressure' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["pressure"],
            'humidity' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["humidity"],
            'max_temp' : city_weather_forecast["data"]["weather"][1]["maxtempC"],
            'min_temp' : city_weather_forecast["data"]["weather"][1]["mintempC"],
            'temperature' : math.ceil(float(city_weather_forecast["data"]["weather"][1]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][1]["mintempC"])/2),
            'description' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["weatherDesc"][0]["value"],
            'icon' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus2d_weather = {
            'weekday' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'date' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'city' : capital_name,     
            'time' : city_weather_forecast["data"]["weather"][2]["date"],
            'pressure' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["pressure"],
            'humidity' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["humidity"],
            'max_temp' : city_weather_forecast["data"]["weather"][2]["maxtempC"],
            'min_temp' : city_weather_forecast["data"]["weather"][2]["mintempC"],
            'temperature' : math.ceil(float(city_weather_forecast["data"]["weather"][2]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][2]["mintempC"])/2),
            'description' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["weatherDesc"][0]["value"],
            'icon' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus3d_weather = {
            'weekday' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'date' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'city' : capital_name,     
            'time' : city_weather_forecast["data"]["weather"][3]["date"],
            'pressure' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["pressure"],
            'humidity' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["humidity"],
            'max_temp' : city_weather_forecast["data"]["weather"][3]["maxtempC"],
            'min_temp' : city_weather_forecast["data"]["weather"][3]["mintempC"],
            'temperature' : math.ceil(float(city_weather_forecast["data"]["weather"][3]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][3]["mintempC"])/2),
            'description' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["weatherDesc"][0]["value"],
            'icon' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus4d_weather = {
            'weekday' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'date' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'city' : capital_name,     
            'time' : city_weather_forecast["data"]["weather"][4]["date"],
            'pressure' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["pressure"],
            'humidity' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["humidity"],
            'max_temp' : city_weather_forecast["data"]["weather"][4]["maxtempC"],
            'min_temp' : city_weather_forecast["data"]["weather"][4]["mintempC"],
            'temperature' : math.ceil(float(city_weather_forecast["data"]["weather"][4]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][4]["mintempC"])/2),
            'description' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["weatherDesc"][0]["value"],
            'icon' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        weather_data_current.append(current_weather) #add the data for the current city into our list
        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_current' : weather_data_current, 'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return render(request, 'country_search/index.html', context) #returns the index.html template
