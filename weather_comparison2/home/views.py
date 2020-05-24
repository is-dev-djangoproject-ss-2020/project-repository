from django.shortcuts import render
import math
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def index(request):
        """This function shows the home page of the whole project."""
        context = {'homepage' : 'homepage'}  
        return render(request, 'home/index.html', context) #returns the index.html template
