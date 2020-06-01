from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
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
    City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    context = {'form' : form}
    return render(request, 'get_json_report/empty.html', context) #returns the index.html template

def openweathermap(request):
    context = openweathermap_processing(request)
    return render(request, 'get_json_report/openweathermap.html', context) #returns the index.html template

def weatherbit(request):
    context = weatherbit_processing(request)
    return render(request, 'get_json_report/weatherbit.html', context) #returns the index.html template

def here(request):
    context = here_processing(request)
    return render(request, 'get_json_report/here.html', context) #returns the index.html template

def worldweatheronline(request):
    context = worldweatheronline_processing(request)
    return render(request, 'get_json_report/worldweatheronline.html', context) #returns the index.html template

def complete(request):
    context = allforecasts_processing(request)
    return render(request, 'get_json_report/complete.html', context) #returns the index.html template