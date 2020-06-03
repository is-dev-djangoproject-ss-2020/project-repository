WEATHER COMPARISON

Background:
	provide extensive capabilities to compare the quality and output of weather forecasts
	part of a student project in "Information Systems Development" at the University Liechtenstein (from March to June 2020)

Contributors: 
	Jann Demond
	Gramoz Sejfijaj
	Mathias Schäfer

System requirements:
	Django framework Version 3.0.5
	Python 3.7

Packages:
	from datetime import datetime
	from datetime import date
	from django.shortcuts import render
	from django.contrib import messages
	import statistics
	import re
	import math
	import requests
	import shutil
	import json
	import time
	import os

Forecast APIs:
	OpenWeatherMap
	Weatherbit
	here.com
	WorldWeatherOnline

Available apps (names as provided in the folder names):
	Weather API 1: type in the name of one city and find out about what our four weather APIs return as the current weather of the city
	Weather API 2: compare the forecasts made by these four providers for the next four days 
	Weather cities: type in the name of various cities and compare the weather in those cities using one of the four available providers
	Weather cities forecast: works like weather cities, but here you can compare the forecasts for the next four days for various cities
	Country search: type in a country name and find out about the current weather (as well as the forecast) in its capital (might be inconsistent if a country does not have full recognition)
	Get JSON report: define a city and get customizable reports about the future weather in JSON forecast
	Forecast evaluation: compare past forecasts for the city and the current weather to see the performance of the forecasts (statistical analysis included)

Usage of city names: 
	For cities and countries, the native name as well as the English name is accepted.
	Cyrilic and Chinese script is accepted for Russian/Chinese city names only.
