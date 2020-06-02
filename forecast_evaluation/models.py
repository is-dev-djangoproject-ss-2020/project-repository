from django.db import models
from datetime import date
import time
import math

# Create your models here.
class City(models.Model):
    """This is a class for storing and processing city names."""
    name = models.CharField(max_length=25)

    def __str__(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'

# models for forecasts:

class Forecast_1_OWM(models.Model):
    """This is a class for storing and processing data from weather forecasts. It is specifically designed for OpenWeatherMap, but inherits its capabilities also the other Forecast classes."""   
    name = models.CharField(max_length=70)
    forecast_provider = models.CharField(max_length=30)
    day_human = models.CharField(max_length=30)
    day_unix = models.IntegerField()
    city = models.CharField(max_length=50)
    countrycode = models.CharField(max_length=50)
    forecast_pressure_1 = models.CharField(max_length=30)
    forecast_humidity_1 = models.CharField(max_length=30)
    forecast_max_temp_1 = models.CharField(max_length=30) 
    forecast_min_temp_1 = models.CharField(max_length=30)
    forecast_temperature_1 = models.CharField(max_length=30)
    forecast_description = models.CharField(max_length=200)
    forecasted_day = models.IntegerField()
    forecast_period = models.IntegerField()
    forecast_icon = models.CharField(max_length=100,default="empty")

    def __str__(self): #show the actual city name on the dashboard
       return self.name
    
    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'forecasts_OWM'

########################

class Forecast_1_Weatherbit(Forecast_1_OWM):
    """This is a class for storing and processing data from weather forecasts from Weatherbit. Its properties are primarily inherited from the Forecast_1_OWM class."""
    def __str__(self): #show the actual city name on the dashboard
       return self.name
    
    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'forecasts_Weatherbit'

######################

class Forecast_1_here(Forecast_1_OWM):
    """This is a class for storing and processing data from weather forecasts from here.com. Its properties are primarily inherited from the Forecast_1_OWM class."""
    def __str__(self): #show the actual city name on the dashboard
       return self.name
    
    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'forecasts_here'

######################

class Forecast_1_WWO(Forecast_1_OWM):
    """This is a class for storing and processing data from weather forecasts from WorldWeatherOnline. Its properties are primarily inherited from the Forecast_1_OWM class."""
    def __str__(self): #show the actual city name on the dashboard
       return self.name
    
    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'forecasts_WWO'
