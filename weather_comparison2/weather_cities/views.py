from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from .processing import openweathermap_current_processing
from .processing import weatherbit_processing
from .processing import here_processing
from .processing import worldweatheronline_processing
from .processing2 import openweathermap_forecast
from .processing2 import weatherbit_forecast
from .processing2 import here_forecast
from .processing2 import worldweatheronline_forecast
from datetime import datetime
import re

def index(request):
    context = openweathermap_current_processing(request)
    return render(request, 'weather_cities/index.html', context) #returns the index.html template

def delete_page_openweathermap(request):
    City.objects.all().delete()
    context = openweathermap_current_processing(request)
    return render(request, 'weather_cities/delete_page_openweathermap.html', context) #returns the index.html template

def weatherbit(request):
    context = weatherbit_processing(request)
    return render(request, 'weather_cities/weatherbit.html', context) #returns the index.html template

def delete_page_weatherbit(request):
    City.objects.all().delete()
    context = weatherbit_processing(request)
    return render(request, 'weather_cities/delete_page_weatherbit.html', context) #returns the index.html template

def here(request):
    context = here_processing(request)
    return render(request, 'weather_cities/here.html', context) #returns the index.html template

def delete_page_here(request):
    City.objects.all().delete()
    context = here_processing(request)
    return render(request, 'weather_cities/delete_page_here.html', context) #returns the index.html template

def worldweatheronline(request):
    context = worldweatheronline_processing(request)
    return render(request, 'weather_cities/worldweatheronline.html', context) #returns the index.html template

def delete_page_worldweatheronline(request):
    City.objects.all().delete()
    context = worldweatheronline_processing(request)
    return render(request, 'weather_cities/delete_page_worldweatheronline.html', context) #returns the index.html template

################
