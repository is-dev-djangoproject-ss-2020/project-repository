from django.shortcuts import render
import math
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def openweathermap_current_processing(request):
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
            'openweathermap_city' : city,
            'openweathermap_countrycode' : city_countrycode,           
            'openweathermap_utc_time' : datetime.utcfromtimestamp(float(city_weather['current']['dt'])).strftime('%Y-%m-%d %H:%M:%S'),
            'openweathermap_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'openweathermap_local_time' : datetime.utcfromtimestamp(float(city_weather['current']['dt']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S'),
            'openweathermap_pressure' : city_weather['current']['pressure'],
            'openweathermap_humidity' : city_weather['current']['humidity'],
            'openweathermap_temperature' : city_weather['current']['temp'],
            'openweathermap_description' : city_weather['current']['weather'][0]['description'],
            'openweathermap_icon' : city_weather['current']['weather'][0]['icon'],
        }

        weather_data.append(weather) #add the data for the current city into our list
        
    context = {'weather_data_openweathermap' : weather_data, 'form' : form}  
    return context #returns the index.html template

#######################

def weatherbit_processing(request):
    City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    url_weather_current = 'https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json()
        city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json()
        
        current_weather = {
            'weatherbit_city' : city,
            'weatherbit_countrycode' : city_countrycode,           
            'weatherbit_utc_time' : datetime.utcfromtimestamp(float(city_weather_current['data'][0]['ts'])).strftime('%Y-%m-%d %H:%M:%S'),
            'weatherbit_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'weatherbit_local_time' : datetime.utcfromtimestamp(float(city_weather_current['data'][0]['ts']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S'),
            'weatherbit_pressure' : city_weather_current['data'][0]['pres'],
            'weatherbit_humidity' : city_weather_current['data'][0]['rh'],
            'weatherbit_temperature' : city_weather_current['data'][0]['temp'],
            'weatherbit_description' : city_weather_current['data'][0]['weather']['description'],
            'weatherbit_icon' : city_weather_current['data'][0]['weather']['icon'],
        }

        weather_data_current.append(current_weather) #add the data for the current city into our list

    context = {'weather_data_current_weatherbit' : weather_data_current, 'form' : form}
    return context

#####################

def here_processing(request):
    City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=forecast_7days_simple&latitude={}&longitude={}'
    url_weather_current = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=observation&latitude={}&longitude={}'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json()
        city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json()

        time_var = re.sub('T',' ',city_weather_current['observations']['location'][0]['observation'][0]['utcTime'])
        local_time = time_var[:-10]
        import datetime
        date_time_obj = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        import time
        unixtime = time.mktime(date_time_obj.timetuple())
        unixtime_2 = unixtime - float(city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])
        date_time_obj_2 = datetime.datetime.fromtimestamp(unixtime_2).strftime('%Y-%m-%d %H:%M:%S')

        icon_link_current=city_weather_current['observations']['location'][0]['observation'][0]['iconLink']
        if icon_link_current == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_current = 3
        else:
            icon_code_current=int(''.join(filter(str.isdigit, icon_link_current)))

        current_weather = {
            'here_city' : city,
            'here_countrycode' : city_countrycode,           
            'here_utc_time' : str(date_time_obj_2),
            'here_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'here_local_time' : str(date_time_obj),
            'here_pressure' : city_weather_current['observations']['location'][0]['observation'][0]['barometerPressure'],
            'here_humidity' : city_weather_current['observations']['location'][0]['observation'][0]['humidity'],
            'here_temperature' : city_weather_current['observations']['location'][0]['observation'][0]['temperature'],
            'here_description' : city_weather_current['observations']['location'][0]['observation'][0]['description'],
            'here_icon' : icon_code_current,
        }

        weather_data_current.append(current_weather) #add the data for the current city into our list

    context = {'weather_data_current_here' : weather_data_current, 'form' : form}  
    return context #returns the index.html template

##################

def worldweatheronline_processing(request):
    City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    #url_weather_current = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=observation&latitude={}&longitude={}'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json()
     #   city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json()

        current_weather = {
            'worldweatheronline_city' : city,
            'worldweatheronline_countrycode' : city_countrycode,           
            'worldweatheronline_utc_time' : city_weather_forecast["data"]["current_condition"][0]["observation_time"],
            'worldweatheronline_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'worldweatheronline_local_time' : city_weather_forecast["data"]["current_condition"][0]["localObsDateTime"],
            'worldweatheronline_pressure' : city_weather_forecast["data"]["current_condition"][0]["pressure"],
            'worldweatheronline_humidity' : city_weather_forecast["data"]["current_condition"][0]["humidity"],
            'worldweatheronline_temperature' : city_weather_forecast["data"]["current_condition"][0]["temp_C"],
            'worldweatheronline_description' : city_weather_forecast["data"]["current_condition"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon' : city_weather_forecast["data"]["current_condition"][0]["weatherIconUrl"][0]["value"],
        }

        weather_data_current.append(current_weather) #add the data for the current city into our list

    context = {'weather_data_current_worldweatheronline' : weather_data_current, 'form' : form}  
    return context #returns the index.html template

#####################

from django.shortcuts import render
from django.contrib import messages
import math
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def current_weather_processing(request):
    City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'
    url_weather_1 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_2 = 'https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M'
    url_weather_3 = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=observation&latitude={}&longitude={}'
    url_weather_4 = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()
    
    weather_data = []

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

        from datetime import datetime
        openweathermap_utc_time = datetime.utcfromtimestamp(float(city_weather_1['current']['dt'])).strftime('%Y-%m-%d %H:%M:%S')
        openweathermap_local_time = datetime.utcfromtimestamp(float(city_weather_1['current']['dt']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S')
        weatherbit_utc_time = datetime.utcfromtimestamp(float(city_weather_2['data'][0]['ts'])).strftime('%Y-%m-%d %H:%M:%S')
        weatherbit_local_time = datetime.utcfromtimestamp(float(city_weather_2['data'][0]['ts']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S')
        
        time_var = re.sub('T',' ',city_weather_3['observations']['location'][0]['observation'][0]['utcTime'])
        local_time = time_var[:-10]
        import datetime
        date_time_obj = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
        import time
        unixtime = time.mktime(date_time_obj.timetuple())
        unixtime_2 = unixtime - float(city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])
        date_time_obj_2 = datetime.datetime.fromtimestamp(unixtime_2).strftime('%Y-%m-%d %H:%M:%S')

        icon_link_current=city_weather_3['observations']['location'][0]['observation'][0]['iconLink']
        if icon_link_current == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_current = 3
        else:
            icon_code_current=int(''.join(filter(str.isdigit, icon_link_current)))

        weather = {
            'openweathermap_provider' : 'OpenWeatherMap',
            'openweathermap_city' : city,
            'openweathermap_countrycode' : city_countrycode,           
            'openweathermap_utc_time' : openweathermap_utc_time,
            'openweathermap_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'openweathermap_local_time' : openweathermap_local_time,
            'openweathermap_pressure' : city_weather_1['current']['pressure'],
            'openweathermap_humidity' : city_weather_1['current']['humidity'],
            'openweathermap_temperature' : city_weather_1['current']['temp'],
            'openweathermap_description' : city_weather_1['current']['weather'][0]['description'],
            'openweathermap_icon' : city_weather_1['current']['weather'][0]['icon'],
            'weatherbit_provider' : 'Weatherbit',
            'weatherbit_city' : city,
            'weatherbit_countrycode' : city_countrycode,           
            'weatherbit_utc_time' : weatherbit_utc_time,
            'weatherbit_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'weatherbit_local_time' : weatherbit_local_time,
            'weatherbit_pressure' : city_weather_2['data'][0]['pres'],
            'weatherbit_humidity' : city_weather_2['data'][0]['rh'],
            'weatherbit_temperature' : city_weather_2['data'][0]['temp'],
            'weatherbit_description' : city_weather_2['data'][0]['weather']['description'],
            'weatherbit_icon' : city_weather_2['data'][0]['weather']['icon'],
            'here_provider' : 'here.com',
            'here_city' : city,
            'here_countrycode' : city_countrycode,           
            'here_utc_time' : str(date_time_obj_2),
            'here_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'here_local_time' : str(date_time_obj),
            'here_pressure' : city_weather_3['observations']['location'][0]['observation'][0]['barometerPressure'],
            'here_humidity' : city_weather_3['observations']['location'][0]['observation'][0]['humidity'],
            'here_temperature' : city_weather_3['observations']['location'][0]['observation'][0]['temperature'],
            'here_description' : city_weather_3['observations']['location'][0]['observation'][0]['description'],
            'here_icon' : icon_code_current,
            'worldweatheronline_provider' : 'WorldWeatherOnline',
            'worldweatheronline_city' : city,
            'worldweatheronline_countrycode' : city_countrycode,           
            'worldweatheronline_utc_time' : city_weather_4["data"]["current_condition"][0]["observation_time"],
            'worldweatheronline_time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'worldweatheronline_local_time' : city_weather_4["data"]["current_condition"][0]["localObsDateTime"],
            'worldweatheronline_pressure' : city_weather_4["data"]["current_condition"][0]["pressure"],
            'worldweatheronline_humidity' : city_weather_4["data"]["current_condition"][0]["humidity"],
            'worldweatheronline_temperature' : city_weather_4["data"]["current_condition"][0]["temp_C"],
            'worldweatheronline_description' : city_weather_4["data"]["current_condition"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon' : city_weather_4["data"]["current_condition"][0]["weatherIconUrl"][0]["value"],
        }

        weather_data.append(weather) #add the data for the current city into our list
        
    context = {'weather_data_current' : weather_data, 'form' : form}  
    return context #returns the index.html template
