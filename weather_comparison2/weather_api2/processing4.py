import re
import math
import requests

from django.shortcuts import render
from django.contrib import messages
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .calendar_tool import calendar_values
from .calendar_tool import date_converter

def openweathermap_processing(request):
    """Retrieves the weather data from OpenWeatherMap and extracts and stores the forecast data."""
    City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = [] #open up the containers to where the weather data will be saved
    weather_data_plus1d = []
    weather_data_plus2d = []
    weather_data_plus3d = []
    weather_data_plus4d = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extraction of latitude and longitude values
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather = requests.get(url_weather.format(lat_param,lng_param)).json() #specification of the URL for OpenWeatherMap

        plus1d_weather = {
            'openweathermap_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'openweathermap_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'openweathermap_city_1' : city,
            'openweathermap_countrycode_1' : city_countrycode,      
            'openweathermap_time_1' : city_weather['daily'][1]['dt'],
            'openweathermap_pressure_1' : city_weather['daily'][1]['pressure'],
            'openweathermap_humidity_1' : city_weather['daily'][1]['humidity'],
            'openweathermap_max_temp_1' : city_weather['daily'][1]['temp']['max'],
            'openweathermap_min_temp_1' : city_weather['daily'][1]['temp']['min'],
            'openweathermap_temperature_1' : city_weather['daily'][1]['temp']['day'],
            'openweathermap_description_1' : city_weather['daily'][1]['weather'][0]['description'],
            'openweathermap_icon_1' : city_weather['daily'][1]['weather'][0]['icon'],
        }

        plus2d_weather = {
            'openweathermap_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'openweathermap_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'openweathermap_city_2' : city,
            'openweathermap_countrycode_2' : city_countrycode,
            'openweathermap_time_2' : city_weather['daily'][2]['dt'],
            'openweathermap_pressure_2' : city_weather['daily'][2]['pressure'],
            'openweathermap_humidity_2' : city_weather['daily'][2]['humidity'],
            'openweathermap_max_temp_2' : city_weather['daily'][2]['temp']['max'],
            'openweathermap_min_temp_2' : city_weather['daily'][2]['temp']['min'],
            'openweathermap_temperature_2' : city_weather['daily'][2]['temp']['day'],
            'openweathermap_description_2' : city_weather['daily'][2]['weather'][0]['description'],
            'openweathermap_icon_2' : city_weather['daily'][2]['weather'][0]['icon'],
        }

        plus3d_weather = {
            'openweathermap_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'openweathermap_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'openweathermap_city_3' : city,
            'openweathermap_countrycode_3' : city_countrycode,
            'openweathermap_time_3' : city_weather['daily'][3]['dt'],
            'openweathermap_pressure_3' : city_weather['daily'][3]['pressure'],
            'openweathermap_humidity_3' : city_weather['daily'][3]['humidity'],
            'openweathermap_max_temp_3' : city_weather['daily'][3]['temp']['max'],
            'openweathermap_min_temp_3' : city_weather['daily'][3]['temp']['min'],
            'openweathermap_temperature_3' : city_weather['daily'][3]['temp']['day'],
            'openweathermap_description_3' : city_weather['daily'][3]['weather'][0]['description'],
            'openweathermap_icon_3' : city_weather['daily'][3]['weather'][0]['icon'],
        }

        plus4d_weather = {
            'openweathermap_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'openweathermap_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'openweathermap_city_4' : city,
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
        
        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return context

###################

def weatherbit_processing(request):
    """Retrieves the weather data from Weatherbit and extracts and stores the forecast data."""
    City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    url_weather_current = 'https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = [] #open up the containers to where the weather data will be saved
    weather_data_plus1d = []
    weather_data_plus2d = []
    weather_data_plus3d = []
    weather_data_plus4d = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extraction of latitude and longitude values
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json() #import future weather data
        city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json() #import current weather data

        plus1d_weather = {
            'weatherbit_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'weatherbit_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'weatherbit_city_1' : city,
            'weatherbit_countrycode_1' : city_countrycode,      
            'weatherbit_time_1' : city_weather_forecast['data'][1]['ts'],
            'weatherbit_pressure_1' : city_weather_forecast['data'][1]['pres'],
            'weatherbit_humidity_1' : city_weather_forecast['data'][1]['rh'],
            'weatherbit_max_temp_1' : city_weather_forecast['data'][1]['max_temp'],
            'weatherbit_min_temp_1' : city_weather_forecast['data'][1]['min_temp'],
            'weatherbit_temperature_1' : city_weather_forecast['data'][1]['temp'],
            'weatherbit_description_1' : city_weather_forecast['data'][1]['weather']['description'],
            'weatherbit_icon_1' : city_weather_forecast['data'][1]['weather']['icon'],
        }

        plus2d_weather = {
            'weatherbit_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'weatherbit_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'weatherbit_city_2' : city,
            'weatherbit_countrycode_2' : city_countrycode,      
            'weatherbit_time_2' : city_weather_forecast['data'][2]['ts'],
            'weatherbit_pressure_2' : city_weather_forecast['data'][2]['pres'],
            'weatherbit_humidity_2' : city_weather_forecast['data'][2]['rh'],
            'weatherbit_max_temp_2' : city_weather_forecast['data'][2]['max_temp'],
            'weatherbit_min_temp_2' : city_weather_forecast['data'][2]['min_temp'],
            'weatherbit_temperature_2' : city_weather_forecast['data'][2]['temp'],
            'weatherbit_description_2' : city_weather_forecast['data'][2]['weather']['description'],
            'weatherbit_icon_2' : city_weather_forecast['data'][2]['weather']['icon'],
        }

        plus3d_weather = {
            'weatherbit_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'weatherbit_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'weatherbit_city_3' : city,
            'weatherbit_countrycode_3' : city_countrycode,      
            'weatherbit_time_3' : city_weather_forecast['data'][3]['ts'],
            'weatherbit_pressure_3' : city_weather_forecast['data'][3]['pres'],
            'weatherbit_humidity_3' : city_weather_forecast['data'][3]['rh'],
            'weatherbit_max_temp_3' : city_weather_forecast['data'][3]['max_temp'],
            'weatherbit_min_temp_3' : city_weather_forecast['data'][3]['min_temp'],
            'weatherbit_temperature_3' : city_weather_forecast['data'][3]['temp'],
            'weatherbit_description_3' : city_weather_forecast['data'][3]['weather']['description'],
            'weatherbit_icon_3' : city_weather_forecast['data'][3]['weather']['icon'],
        }

        plus4d_weather = {
            'weatherbit_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'weatherbit_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'weatherbit_city_4' : city,
            'weatherbit_countrycode_4' : city_countrycode,      
            'weatherbit_time_4' : city_weather_forecast['data'][4]['ts'],
            'weatherbit_pressure_4' : city_weather_forecast['data'][4]['pres'],
            'weatherbit_humidity_4' : city_weather_forecast['data'][4]['rh'],
            'weatherbit_max_temp_4' : city_weather_forecast['data'][4]['max_temp'],
            'weatherbit_min_temp_4' : city_weather_forecast['data'][4]['min_temp'],
            'weatherbit_temperature_4' : city_weather_forecast['data'][4]['temp'],
            'weatherbit_description_4' : city_weather_forecast['data'][4]['weather']['description'],
            'weatherbit_icon_4' : city_weather_forecast['data'][4]['weather']['icon'],
        }
        
        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}
    return context

###################

def here_processing(request):
    """Retrieves the weather data from here.com and extracts and stores the forecast data."""
    City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=forecast_7days_simple&latitude={}&longitude={}'
    url_weather_current = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=observation&latitude={}&longitude={}'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = [] #open up the containers to where the weather data will be saved
    weather_data_plus1d = []
    weather_data_plus2d = []
    weather_data_plus3d = []
    weather_data_plus4d = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        
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

        icon_link_forecast_1=city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['iconLink']
        if icon_link_forecast_1 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_1 = 3
        else:
            icon_code_forecast_1=int(''.join(filter(str.isdigit, icon_link_forecast_1)))

        icon_link_forecast_2=city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['iconLink']
        if icon_link_forecast_2 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_2 = 3
        else:
            icon_code_forecast_2=int(''.join(filter(str.isdigit, icon_link_forecast_2)))

        icon_link_forecast_3=city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['iconLink']
        if icon_link_forecast_3 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_3 = 3
        else:
            icon_code_forecast_3=int(''.join(filter(str.isdigit, icon_link_forecast_3)))

        icon_link_forecast_4=city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['iconLink']
        if icon_link_forecast_4 == "https://weather.ls.hereapi.com/static/weather/icon/blank.png":
            icon_code_forecast_4 = 3
        else:
            icon_code_forecast_4=int(''.join(filter(str.isdigit, icon_link_forecast_4)))

        plus1d_weather = {
            'here_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'here_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'here_city_1' : city,
            'here_countrycode_1' : city_countrycode,      
            'here_time_1' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['utcTime'],
            'here_pressure_1' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['barometerPressure'],
            'here_humidity_1' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['humidity'],
            'here_max_temp_1' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'],
            'here_min_temp_1' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['lowTemperature'],
            'here_temperature_1' : math.ceil(float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['lowTemperature'])/2+float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_1' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['description'],
            'here_icon_1' : icon_code_forecast_1,
        }

        plus2d_weather = {
            'here_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'here_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'here_city_2' : city,
            'here_countrycode_2' : city_countrycode,      
            'here_time_2' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['utcTime'],
            'here_pressure_2' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['barometerPressure'],
            'here_humidity_2' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['humidity'],
            'here_max_temp_2' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['highTemperature'],
            'here_min_temp_2' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['lowTemperature'],
            'here_temperature_2' : math.ceil(float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['lowTemperature'])/2+float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_2' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][2]['description'],
            'here_icon_2' : icon_code_forecast_2,
        }

        plus3d_weather = {
            'here_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'here_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'here_city_3' : city,
            'here_countrycode_3' : city_countrycode,      
            'here_time_3' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['utcTime'],
            'here_pressure_3' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['barometerPressure'],
            'here_humidity_3' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['humidity'],
            'here_max_temp_3' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['highTemperature'],
            'here_min_temp_3' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['lowTemperature'],
            'here_temperature_3' : math.ceil(float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['lowTemperature'])/2+float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_3' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][3]['description'],
            'here_icon_3' : icon_code_forecast_3,
        }

        plus4d_weather = {
            'here_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'here_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'here_city_4' : city,
            'here_countrycode_4' : city_countrycode,      
            'here_time_4' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['utcTime'],
            'here_pressure_4' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['barometerPressure'],
            'here_humidity_4' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['humidity'],
            'here_max_temp_4' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['highTemperature'],
            'here_min_temp_4' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['lowTemperature'],
            'here_temperature_4' : math.ceil(float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['lowTemperature'])/2+float(city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_4' : city_weather_forecast['dailyForecasts']['forecastLocation']['forecast'][4]['description'],
            'here_icon_4' : icon_code_forecast_4,
        }

        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return context 

###################

def worldweatheronline_processing(request):
    """Retrieves the weather data from WorldWeatherOnline and extracts and stores the forecast data."""
    City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather_forecast = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = [] #open up the containers to where the weather data will be saved
    weather_data_plus1d = []
    weather_data_plus2d = []
    weather_data_plus3d = []
    weather_data_plus4d = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            messages.error(request, "Error")
            break
        
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"]) #extraction of latitude and longitude values
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json() #specification of the URL for WorldWeatherOnline
        
        plus1d_weather = {
            'worldweatheronline_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'worldweatheronline_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'worldweatheronline_city_1' : city,
            'worldweatheronline_countrycode_1' : city_countrycode,      
            'worldweatheronline_time_1' : city_weather_forecast["data"]["weather"][1]["date"],
            'worldweatheronline_pressure_1' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_1' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_1' : city_weather_forecast["data"]["weather"][1]["maxtempC"],
            'worldweatheronline_min_temp_1' : city_weather_forecast["data"]["weather"][1]["mintempC"],
            'worldweatheronline_temperature_1' : math.ceil(float(city_weather_forecast["data"]["weather"][1]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][1]["mintempC"])/2),
            'worldweatheronline_description_1' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_1' : city_weather_forecast["data"]["weather"][1]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus2d_weather = {
            'worldweatheronline_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'worldweatheronline_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'worldweatheronline_city_2' : city,
            'worldweatheronline_countrycode_2' : city_countrycode,      
            'worldweatheronline_time_2' : city_weather_forecast["data"]["weather"][2]["date"],
            'worldweatheronline_pressure_2' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_2' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_2' : city_weather_forecast["data"]["weather"][2]["maxtempC"],
            'worldweatheronline_min_temp_2' : city_weather_forecast["data"]["weather"][2]["mintempC"],
            'worldweatheronline_temperature_2' : math.ceil(float(city_weather_forecast["data"]["weather"][2]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][2]["mintempC"])/2),
            'worldweatheronline_description_2' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_2' : city_weather_forecast["data"]["weather"][2]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus3d_weather = {
            'worldweatheronline_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'worldweatheronline_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'worldweatheronline_city_3' : city,
            'worldweatheronline_countrycode_3' : city_countrycode,      
            'worldweatheronline_time_3' : city_weather_forecast["data"]["weather"][3]["date"],
            'worldweatheronline_pressure_3' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_3' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_3' : city_weather_forecast["data"]["weather"][3]["maxtempC"],
            'worldweatheronline_min_temp_3' : city_weather_forecast["data"]["weather"][3]["mintempC"],
            'worldweatheronline_temperature_3' : math.ceil(float(city_weather_forecast["data"]["weather"][3]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][3]["mintempC"])/2),
            'worldweatheronline_description_3' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_3' : city_weather_forecast["data"]["weather"][3]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus4d_weather = {
            'worldweatheronline_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'worldweatheronline_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'worldweatheronline_city_4' : city,
            'worldweatheronline_countrycode_4' : city_countrycode,      
            'worldweatheronline_time_4' : city_weather_forecast["data"]["weather"][4]["date"],
            'worldweatheronline_pressure_4' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_4' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_4' : city_weather_forecast["data"]["weather"][4]["maxtempC"],
            'worldweatheronline_min_temp_4' : city_weather_forecast["data"]["weather"][4]["mintempC"],
            'worldweatheronline_temperature_4' : math.ceil(float(city_weather_forecast["data"]["weather"][4]["maxtempC"])/2+float(city_weather_forecast["data"]["weather"][4]["mintempC"])/2),
            'worldweatheronline_description_4' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_4' : city_weather_forecast["data"]["weather"][4]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return context 

####################

def allforecasts_processing(request):
    """Retrieves the weather data from all available forecast providers and extracts and stores the forecast data."""
    City.objects.all().delete() #(uncomment so that only one city can be used at a time)
    cities = City.objects.all() #return all the cities in the database
    url_weather_1 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_2 = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    url_weather_3 = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=VCeAX-isAP-r2K2JzUfkgMe63dSEAbS-KIO1WUjL0FI&product=forecast_7days_simple&latitude={}&longitude={}'
    url_weather_4 = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=220c64fed4a44bed8d293252201705&q={},{}&num_of_days=5&tp=24&format=json&extra=localObsTime'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_plus1d = [] #open up the containers to where the weather data will be saved
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

        plus1d_weather = {
            'openweathermap_provider_1' : 'OpenWeatherMap',
            'weatherbit_provider_1' : 'Weatherbit',
            'here_provider_1' : 'here.com',
            'worldweatheronline_provider_1' : 'WorldWeatherOnline',
            'openweathermap_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'openweathermap_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'openweathermap_city_1' : city,
            'openweathermap_countrycode_1' : city_countrycode,      
            'openweathermap_time_1' : city_weather_1['daily'][1]['dt'],
            'openweathermap_pressure_1' : city_weather_1['daily'][1]['pressure'],
            'openweathermap_humidity_1' : city_weather_1['daily'][1]['humidity'],
            'openweathermap_max_temp_1' : city_weather_1['daily'][1]['temp']['max'],
            'openweathermap_min_temp_1' : city_weather_1['daily'][1]['temp']['min'],
            'openweathermap_temperature_1' : city_weather_1['daily'][1]['temp']['day'],
            'openweathermap_description_1' : city_weather_1['daily'][1]['weather'][0]['description'],
            'openweathermap_icon_1' : city_weather_1['daily'][1]['weather'][0]['icon'],
            'weatherbit_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'weatherbit_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'weatherbit_city_1' : city,
            'weatherbit_countrycode_1' : city_countrycode,      
            'weatherbit_time_1' : city_weather_2['data'][1]['ts'],
            'weatherbit_pressure_1' : city_weather_2['data'][1]['pres'],
            'weatherbit_humidity_1' : city_weather_2['data'][1]['rh'],
            'weatherbit_max_temp_1' : city_weather_2['data'][1]['max_temp'],
            'weatherbit_min_temp_1' : city_weather_2['data'][1]['min_temp'],
            'weatherbit_temperature_1' : city_weather_2['data'][1]['temp'],
            'weatherbit_description_1' : city_weather_2['data'][1]['weather']['description'],
            'weatherbit_icon_1' : city_weather_2['data'][1]['weather']['icon'],
            'here_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'here_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'here_city_1' : city,
            'here_countrycode_1' : city_countrycode,      
            'here_time_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['utcTime'],
            'here_pressure_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['barometerPressure'],
            'here_humidity_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['humidity'],
            'here_max_temp_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'],
            'here_min_temp_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['lowTemperature'],
            'here_temperature_1' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_1' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['description'],
            'here_icon_1' : icon_code_forecast_1,
            'worldweatheronline_date_1' : calendar_values()['calendar_data'][0]['date_object_tomorrow'],
            'worldweatheronline_weekday_1' : calendar_values()['calendar_data'][0]['weekday_tomorrow'],
            'worldweatheronline_city_1' : city,
            'worldweatheronline_countrycode_1' : city_countrycode,      
            'worldweatheronline_time_1' : city_weather_4["data"]["weather"][1]["date"],
            'worldweatheronline_pressure_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_1' : city_weather_4["data"]["weather"][1]["maxtempC"],
            'worldweatheronline_min_temp_1' : city_weather_4["data"]["weather"][1]["mintempC"],
            'worldweatheronline_temperature_1' : math.ceil(float(city_weather_4["data"]["weather"][1]["maxtempC"])/2+float(city_weather_4["data"]["weather"][1]["mintempC"])/2),
            'worldweatheronline_description_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_1' : city_weather_4["data"]["weather"][1]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus2d_weather = {
            'openweathermap_provider_2' : 'OpenWeatherMap',
            'weatherbit_provider_2' : 'Weatherbit',
            'here_provider_2' : 'here.com',
            'worldweatheronline_provider_2' : 'WorldWeatherOnline',
            'openweathermap_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'openweathermap_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'openweathermap_city_2' : city,
            'openweathermap_countrycode_2' : city_countrycode,
            'openweathermap_time_2' : city_weather_1['daily'][2]['dt'],
            'openweathermap_pressure_2' : city_weather_1['daily'][2]['pressure'],
            'openweathermap_humidity_2' : city_weather_1['daily'][2]['humidity'],
            'openweathermap_max_temp_2' : city_weather_1['daily'][2]['temp']['max'],
            'openweathermap_min_temp_2' : city_weather_1['daily'][2]['temp']['min'],
            'openweathermap_temperature_2' : city_weather_1['daily'][2]['temp']['day'],
            'openweathermap_description_2' : city_weather_1['daily'][2]['weather'][0]['description'],
            'openweathermap_icon_2' : city_weather_1['daily'][2]['weather'][0]['icon'],
            'weatherbit_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'weatherbit_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'weatherbit_city_2' : city,
            'weatherbit_countrycode_2' : city_countrycode,      
            'weatherbit_time_2' : city_weather_2['data'][2]['ts'],
            'weatherbit_pressure_2' : city_weather_2['data'][2]['pres'],
            'weatherbit_humidity_2' : city_weather_2['data'][2]['rh'],
            'weatherbit_max_temp_2' : city_weather_2['data'][2]['max_temp'],
            'weatherbit_min_temp_2' : city_weather_2['data'][2]['min_temp'],
            'weatherbit_temperature_2' : city_weather_2['data'][2]['temp'],
            'weatherbit_description_2' : city_weather_2['data'][2]['weather']['description'],
            'weatherbit_icon_2' : city_weather_2['data'][2]['weather']['icon'],
            'here_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'here_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'here_city_2' : city,
            'here_countrycode_2' : city_countrycode,      
            'here_time_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['utcTime'],
            'here_pressure_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['barometerPressure'],
            'here_humidity_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['humidity'],
            'here_max_temp_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['highTemperature'],
            'here_min_temp_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['lowTemperature'],
            'here_temperature_2' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_2' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][2]['description'],
            'here_icon_2' : icon_code_forecast_2,
            'worldweatheronline_date_2' : calendar_values()['calendar_data'][0]['date_object_in_2_days'],
            'worldweatheronline_weekday_2' : calendar_values()['calendar_data'][0]['weekday_in_2_days'],
            'worldweatheronline_city_2' : city,
            'worldweatheronline_countrycode_2' : city_countrycode,      
            'worldweatheronline_time_2' : city_weather_4["data"]["weather"][2]["date"],
            'worldweatheronline_pressure_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_2' : city_weather_4["data"]["weather"][2]["maxtempC"],
            'worldweatheronline_min_temp_2' : city_weather_4["data"]["weather"][2]["mintempC"],
            'worldweatheronline_temperature_2' : math.ceil(float(city_weather_4["data"]["weather"][2]["maxtempC"])/2+float(city_weather_4["data"]["weather"][2]["mintempC"])/2),
            'worldweatheronline_description_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_2' : city_weather_4["data"]["weather"][2]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus3d_weather = {
            'openweathermap_provider_3' : 'OpenWeatherMap',
            'weatherbit_provider_3' : 'Weatherbit',
            'here_provider_3' : 'here.com',
            'worldweatheronline_provider_3' : 'WorldWeatherOnline',
            'openweathermap_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'openweathermap_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'openweathermap_city_3' : city,
            'openweathermap_countrycode_3' : city_countrycode,
            'openweathermap_time_3' : city_weather_1['daily'][3]['dt'],
            'openweathermap_pressure_3' : city_weather_1['daily'][3]['pressure'],
            'openweathermap_humidity_3' : city_weather_1['daily'][3]['humidity'],
            'openweathermap_max_temp_3' : city_weather_1['daily'][3]['temp']['max'],
            'openweathermap_min_temp_3' : city_weather_1['daily'][3]['temp']['min'],
            'openweathermap_temperature_3' : city_weather_1['daily'][3]['temp']['day'],
            'openweathermap_description_3' : city_weather_1['daily'][3]['weather'][0]['description'],
            'openweathermap_icon_3' : city_weather_1['daily'][3]['weather'][0]['icon'],
            'weatherbit_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'weatherbit_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'weatherbit_city_3' : city,
            'weatherbit_countrycode_3' : city_countrycode,      
            'weatherbit_time_3' : city_weather_2['data'][3]['ts'],
            'weatherbit_pressure_3' : city_weather_2['data'][3]['pres'],
            'weatherbit_humidity_3' : city_weather_2['data'][3]['rh'],
            'weatherbit_max_temp_3' : city_weather_2['data'][3]['max_temp'],
            'weatherbit_min_temp_3' : city_weather_2['data'][3]['min_temp'],
            'weatherbit_temperature_3' : city_weather_2['data'][3]['temp'],
            'weatherbit_description_3' : city_weather_2['data'][3]['weather']['description'],
            'weatherbit_icon_3' : city_weather_2['data'][3]['weather']['icon'],
            'here_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'here_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'here_city_3' : city,
            'here_countrycode_3' : city_countrycode,      
            'here_time_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['utcTime'],
            'here_pressure_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['barometerPressure'],
            'here_humidity_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['humidity'],
            'here_max_temp_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['highTemperature'],
            'here_min_temp_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['lowTemperature'],
            'here_temperature_3' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_3' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][3]['description'],
            'here_icon_3' : icon_code_forecast_3,
            'worldweatheronline_date_3' : calendar_values()['calendar_data'][0]['date_object_in_3_days'],
            'worldweatheronline_weekday_3' : calendar_values()['calendar_data'][0]['weekday_in_3_days'],
            'worldweatheronline_city_3' : city,
            'worldweatheronline_countrycode_3' : city_countrycode,      
            'worldweatheronline_time_3' : city_weather_4["data"]["weather"][3]["date"],
            'worldweatheronline_pressure_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_3' : city_weather_4["data"]["weather"][3]["maxtempC"],
            'worldweatheronline_min_temp_3' : city_weather_4["data"]["weather"][3]["mintempC"],
            'worldweatheronline_temperature_3' : math.ceil(float(city_weather_4["data"]["weather"][3]["maxtempC"])/2+float(city_weather_4["data"]["weather"][3]["mintempC"])/2),
            'worldweatheronline_description_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_3' : city_weather_4["data"]["weather"][3]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        plus4d_weather = {
            'openweathermap_provider_4' : 'OpenWeatherMap',
            'weatherbit_provider_4' : 'Weatherbit',
            'here_provider_4' : 'here.com',
            'worldweatheronline_provider_4' : 'WorldWeatherOnline',
            'openweathermap_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'openweathermap_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'openweathermap_city_4' : city,
            'openweathermap_countrycode_4' : city_countrycode,
            'openweathermap_time_4' : city_weather_1['daily'][4]['dt'],
            'openweathermap_pressure_4' : city_weather_1['daily'][4]['pressure'],
            'openweathermap_humidity_4' : city_weather_1['daily'][4]['humidity'],
            'openweathermap_max_temp_4' : city_weather_1['daily'][4]['temp']['max'],
            'openweathermap_min_temp_4' : city_weather_1['daily'][4]['temp']['min'],
            'openweathermap_temperature_4' : city_weather_1['daily'][4]['temp']['day'],
            'openweathermap_description_4' : city_weather_1['daily'][4]['weather'][0]['description'],
            'openweathermap_icon_4' : city_weather_1['daily'][4]['weather'][0]['icon'],
            'weatherbit_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'weatherbit_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'weatherbit_city_4' : city,
            'weatherbit_countrycode_4' : city_countrycode,      
            'weatherbit_time_4' : city_weather_2['data'][4]['ts'],
            'weatherbit_pressure_4' : city_weather_2['data'][4]['pres'],
            'weatherbit_humidity_4' : city_weather_2['data'][4]['rh'],
            'weatherbit_max_temp_4' : city_weather_2['data'][4]['max_temp'],
            'weatherbit_min_temp_4' : city_weather_2['data'][4]['min_temp'],
            'weatherbit_temperature_4' : city_weather_2['data'][4]['temp'],
            'weatherbit_description_4' : city_weather_2['data'][4]['weather']['description'],
            'weatherbit_icon_4' : city_weather_2['data'][4]['weather']['icon'],
            'here_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'here_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'here_city_4' : city,
            'here_countrycode_4' : city_countrycode,      
            'here_time_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['utcTime'],
            'here_pressure_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['barometerPressure'],
            'here_humidity_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['humidity'],
            'here_max_temp_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['highTemperature'],
            'here_min_temp_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['lowTemperature'],
            'here_temperature_4' : math.ceil(float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['lowTemperature'])/2+float(city_weather_3['dailyForecasts']['forecastLocation']['forecast'][1]['highTemperature'])/2),
            'here_description_4' : city_weather_3['dailyForecasts']['forecastLocation']['forecast'][4]['description'],
            'here_icon_4' : icon_code_forecast_4,
            'worldweatheronline_date_4' : calendar_values()['calendar_data'][0]['date_object_in_4_days'],
            'worldweatheronline_weekday_4' : calendar_values()['calendar_data'][0]['weekday_in_4_days'],
            'worldweatheronline_city_4' : city,
            'worldweatheronline_countrycode_4' : city_countrycode,      
            'worldweatheronline_time_4' : city_weather_4["data"]["weather"][4]["date"],
            'worldweatheronline_pressure_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["pressure"],
            'worldweatheronline_humidity_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["humidity"],
            'worldweatheronline_max_temp_4' : city_weather_4["data"]["weather"][4]["maxtempC"],
            'worldweatheronline_min_temp_4' : city_weather_4["data"]["weather"][4]["mintempC"],
            'worldweatheronline_temperature_4' : math.ceil(float(city_weather_4["data"]["weather"][4]["maxtempC"])/2+float(city_weather_4["data"]["weather"][4]["mintempC"])/2),
            'worldweatheronline_description_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["weatherDesc"][0]["value"],
            'worldweatheronline_icon_4' : city_weather_4["data"]["weather"][4]["hourly"][0]["weatherIconUrl"][0]["value"],
        }

        calendar = {
            'date_converted_1' : date_converter(1),
            'date_converted_2' : date_converter(2),
            'date_converted_3' : date_converter(3),
            'date_converted_4' : date_converter(4),
        }

        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        calendar_data.append(calendar)
        
    context = {'calendar_data' : calendar_data, 'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return context
