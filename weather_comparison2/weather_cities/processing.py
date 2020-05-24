from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def openweathermap_current_processing(request):
    """Retrieves the weather data from OpenWeatherMap, saving the relevant current weather data."""
    #City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()
    
    weather_data_id_1 = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extraction of latitude and longitude values
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"]) #extraction of latitude and longitude values

        city_weather = requests.get(url_weather.format(lat_param,lng_param)).json() #specification of the URL for OpenWeatherMap
        
        weather = {
            'provider': 'OpenWeatherMap',
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

        weather_data_id_1.append(weather) #add the data for the current city into our list
        
    context = {'weather_data_id_1' : weather_data_id_1, 'form' : form}  
    return context 

#############################

def weatherbit_processing(request):
    """Retrieves the weather data from Weatherbit, saving the relevant current weather data."""
    #City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather_forecast = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    url_weather_current = 'https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_id_1 = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extraction of latitude and longitude values
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json() #specification of the URL for Weatherbit
        city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json() #specification of the URL for Weatherbit
        
        weather = {
            'provider': 'Weatherbit',
            'city' : city,
            'countrycode' : city_countrycode,           
            'utc_time' : datetime.utcfromtimestamp(float(city_weather_current['data'][0]['ts'])).strftime('%Y-%m-%d %H:%M:%S'),
            'time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'local_time' : datetime.utcfromtimestamp(float(city_weather_current['data'][0]['ts']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S'),
            'pressure' : city_weather_current['data'][0]['pres'],
            'humidity' : city_weather_current['data'][0]['rh'],
            'temperature' : city_weather_current['data'][0]['temp'],
            'description' : city_weather_current['data'][0]['weather']['description'],
            'icon' : city_weather_current['data'][0]['weather']['icon'],
        }

        weather_data_id_1.append(weather) #add the data for the current city into our list

    context = {'weather_data_id_1' : weather_data_id_1, 'form' : form}
    return context

############################

def here_processing(request):
    """Retrieves the weather data from here.com, saving the relevant current weather data."""
    #City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather_forecast = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=forecast_7days_simple&latitude={}&longitude={}'
    url_weather_current = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=observation&latitude={}&longitude={}'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_id_1 = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extraction of latitude and longitude values
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"]) #extraction of latitude and longitude values

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json() #specification of the URL for here.com
        city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json() #specification of the URL for here.com

        time_var = re.sub('T',' ',city_weather_current['observations']['location'][0]['observation'][0]['utcTime']) #adapt the format of the timestamp
        local_time = time_var[:-10]
        import datetime
        date_time_obj = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        import time
        unixtime = time.mktime(date_time_obj.timetuple())
        unixtime_2 = unixtime - float(city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"]) #correct for timezone
        date_time_obj_2 = datetime.datetime.fromtimestamp(unixtime_2).strftime('%Y-%m-%d %H:%M:%S')

        icon_link_current=city_weather_current['observations']['location'][0]['observation'][0]['iconLink']
        if icon_link_current == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_current = 3
        else:
            icon_code_current=int(''.join(filter(str.isdigit, icon_link_current)))

        weather = {
            'provider': 'here.com',
            'city' : city,
            'countrycode' : city_countrycode,           
            'utc_time' : str(date_time_obj_2),
            'time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'local_time' : str(date_time_obj),
            'pressure' : city_weather_current['observations']['location'][0]['observation'][0]['barometerPressure'],
            'humidity' : city_weather_current['observations']['location'][0]['observation'][0]['humidity'],
            'temperature' : city_weather_current['observations']['location'][0]['observation'][0]['temperature'],
            'description' : city_weather_current['observations']['location'][0]['observation'][0]['description'],
            'icon' : icon_code_current,
        }

        weather_data_id_1.append(weather) #add the data for the current city into our list

    context = {'weather_data_id_1' : weather_data_id_1, 'form' : form}  
    return context #returns the index.html template

#############################

def worldweatheronline_processing(request):
    """Retrieves the weather data from WorldWeatherOnline, saving the relevant current weather data."""
    #City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather_forecast = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_id_1 = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extract the values for longitude and latitude
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"]) #extract the values for longitude and latitude

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json() #specification of the URL for WorldWeatherOnline

        weather = {
            'provider': 'WorldWeatherOnline',
            'city' : city,
            'countrycode' : city_countrycode,           
            'utc_time' : city_weather_forecast["data"]["current_condition"][0]["observation_time"],
            'time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'local_time' : city_weather_forecast["data"]["current_condition"][0]["localObsDateTime"],
            'pressure' : city_weather_forecast["data"]["current_condition"][0]["pressure"],
            'humidity' : city_weather_forecast["data"]["current_condition"][0]["humidity"],
            'temperature' : city_weather_forecast["data"]["current_condition"][0]["temp_C"],
            'description' : city_weather_forecast["data"]["current_condition"][0]["weatherDesc"][0]["value"],
            'icon' : city_weather_forecast["data"]["current_condition"][0]["weatherIconUrl"][0]["value"],
        }

        weather_data_id_1.append(weather) #add the data for the current city into our list

    context = {'weather_data_id_1' : weather_data_id_1, 'form' : form}  
    return context

