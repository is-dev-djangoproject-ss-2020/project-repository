from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
from .processing3 import current_weather_processing
from .processing4 import evaluation
from .calendar_tool import calendar_values
from .calendar_tool import date_converter
import re

def index(request):
    """Shows the index page of the forecast_evaluation app."""
    context = current_weather_processing(request)
    return render(request, 'forecast_evaluation/index.html', context) #returns the index.html template

def delete_page(request):
    """Shows the delete page of the forecast_evaluation app, but this page is only expected to be used by the developers."""
    context = current_weather_processing(request)
    City.objects.all().delete()
    return render(request, 'forecast_evaluation/delete_page.html', context) #returns the index.html template

def city_page(request):
    """Shows the overview of all cities currently maintained by the project."""
    return render(request, 'forecast_evaluation/city_page.html') #returns the index.html template

def forecast_evaluation_bludenz(request):
    """Shows the overview of past forecast and current weather in Bludenz."""
    context = evaluation(request,"Bludenz")
    return render(request, 'forecast_evaluation/forecast_evaluation_bludenz.html', context) #returns the index.html template

def forecast_evaluation_vaduz(request):
    """Shows the overview of past forecast and current weather in Vaduz."""
    context = evaluation(request,"Vaduz")
    return render(request, 'forecast_evaluation/forecast_evaluation_vaduz.html', context) #returns the index.html template

def forecast_evaluation_zurich(request):
    """Shows the overview of past forecast and current weather in Zurich."""
    context = evaluation(request,"Zurich")
    return render(request, 'forecast_evaluation/forecast_evaluation_zurich.html', context) #returns the index.html template

def forecast_evaluation_oslo(request):
    """Shows the overview of past forecast and current weather in Oslo."""
    context = evaluation(request,"Oslo")
    return render(request, 'forecast_evaluation/forecast_evaluation_oslo.html', context) #returns the index.html template

def forecast_evaluation_madrid(request):
    """Shows the overview of past forecast and current weather in Madrid."""
    context = evaluation(request,"Madrid")
    return render(request, 'forecast_evaluation/forecast_evaluation_madrid.html', context) #returns the index.html template

def forecast_evaluation_paris(request):
    """Shows the overview of past forecast and current weather in Paris."""
    context = evaluation(request,"Paris")
    return render(request, 'forecast_evaluation/forecast_evaluation_paris.html', context) #returns the index.html template
