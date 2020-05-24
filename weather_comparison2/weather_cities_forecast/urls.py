from django.urls import path
from . import views

app_name = 'weather_cities_forecast'
urlpatterns = [
    path('index_forecast', views.index_forecast, name="index_forecast"),  #the path for our index view 
    path('delete_page_openweathermap_forecast', views.delete_page_openweathermap_forecast, name="delete_page_openweathermap_forecast"),  
]
