from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from .processing2 import openweathermap_forecast
from datetime import datetime
import re

################

def index_forecast(request):
    """Creates the view for the forecast comparison"""
    context = openweathermap_forecast(request)
    return render(request, 'weather_cities_forecast/index_forecast.html', context) #returns the index.html template

def delete_page_openweathermap_forecast(request):
    """Creates the view for the page where cities can be deleted."""
    City.objects.all().delete()
    context = openweathermap_forecast(request)
    return render(request, 'weather_cities_forecast/delete_page_openweathermap_forecast.html', context) #returns the index.html template
