from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import math
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def index(request):
        weather_data_current = []
        current_weather = {
            'city' : 'text1',
            'countrycode' : 'text1',           
            'utc_time' : 'text1',
            'time_zone' : 'text1',
            'local_time' : 'text1',
            'pressure' : 'text1',
            'humidity' : 'text1',
            'temperature' : 'text1',
            'description' : 'text1',
            'icon' : 'text1',
        }

        weather_data_current.append(current_weather) #add the data for the current city into our list

        context = {'weather_data_current' : weather_data_current}  
        return render(request, 'home/index.html', context) #returns the index.html template
