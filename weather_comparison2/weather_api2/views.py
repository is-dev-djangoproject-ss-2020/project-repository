from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .processing4 import openweathermap_processing
from .processing4 import weatherbit_processing
from .processing4 import here_processing
from .processing4 import worldweatheronline_processing
from .processing4 import allforecasts_processing
import re

def index(request):
    context = openweathermap_processing(request)
    return render(request, 'weather_api2/index.html', context) #returns the index.html template

def weatherbit(request):
    context = weatherbit_processing(request)
    return render(request, 'weather_api2/weatherbit.html', context) #returns the index.html template

def here(request):
    context = here_processing(request)
    return render(request, 'weather_api2/here.html', context) #returns the index.html template

def worldweatheronline(request):
    context = worldweatheronline_processing(request)
    return render(request, 'weather_api2/worldweatheronline.html', context) #returns the index.html template

def all_on_one_page(request):
    context = allforecasts_processing(request)
    return render(request, 'weather_api2/all_on_one_page.html', context) #returns the index.html template
