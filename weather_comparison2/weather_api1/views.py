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
from .calendar_tool import calendar_values
from .calendar_tool import date_converter
import re

def index(request):
    """Provides the index page for the current weather comparison application."""
    context = current_weather_processing(request)
    return render(request, 'weather_api1/index.html', context) #returns the index.html template
