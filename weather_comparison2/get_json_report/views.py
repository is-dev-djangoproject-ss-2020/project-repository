from django.shortcuts import render
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .calendar_tool import calendar_values
from .calendar_tool import date_converter
from .processing_json_complete import allforecasts_processing
from .processing_json_openweathermap import openweathermap_processing
from .processing_json_weatherbit import weatherbit_processing
from .processing_json_here import here_processing
from .processing_json_worldweatheronline import worldweatheronline_processing
import re

def empty(request):
    """Provides the overview page of this section where the demanded city and the provider can be chosen."""
    City.objects.all().delete() #existing city objects are deleted every time this page is called
    cities = City.objects.all() #creates a list object where the chosen cities can be saved to
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm() # show an empty field for entering more cities (if desired)

    message_dict = {}
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        if city_geodata["total_results"] == 0:
            "City"+str(city.name)+"has been selected!"
            message_dict = {'message' : "City"+str(city.name)+"is invalid!"}
            break
        else:
            message_dict = {'message' : "City"+str(city.name)+"has been selected!"}

    context = {'message_dict' : message_dict, 'form' : form}
    return render(request, 'get_json_report/empty.html', context) #returns the index.html template

def openweathermap(request):
    """Executes the rendering for the page, where the JSON report based on OpenWeatherMap can be generated."""
    context = openweathermap_processing(request)
    return render(request, 'get_json_report/openweathermap.html', context) #download the report for the openweathermap forecast

def weatherbit(request):
    """Executes the rendering for the page, where the JSON report based on Weatherbit can be generated."""
    context = weatherbit_processing(request)
    return render(request, 'get_json_report/weatherbit.html', context) #download the report for the weatherbit forecast

def here(request):
    """Executes the rendering for the page, where the JSON report based on here.com can be generated."""
    context = here_processing(request)
    return render(request, 'get_json_report/here.html', context) #download the report for the here.com forecast

def worldweatheronline(request):
    """Executes the rendering for the page, where the JSON report based on WorldWeatherOnline can be generated."""
    context = worldweatheronline_processing(request)
    return render(request, 'get_json_report/worldweatheronline.html', context) #download the report for the WorldWeatherOnline forecast

def complete(request):
    "returns the view, where the outputs of all forecasts can be retrieved and downloaded."
    context = allforecasts_processing(request)
    return render(request, 'get_json_report/complete.html', context) #returns the view, where the outputs of all forecasts can be retrieved and downloaded
