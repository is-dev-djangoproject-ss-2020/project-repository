from django.urls import path
from . import views

app_name = 'weather_cities'
urlpatterns = [
    path('', views.index, name="index"),  #the path for our index view
    path('weatherbit', views.weatherbit, name="weatherbit"),
    path('here', views.here, name="here"),
    path('worldweatheronline', views.worldweatheronline, name="worldweatheronline"),  
    path('delete_page_openweathermap', views.delete_page_openweathermap, name="delete_page_openweathermap"),  
    path('delete_page_weatherbit', views.delete_page_weatherbit, name="delete_page_weatherbit"), 
    path('delete_page_here', views.delete_page_here, name="delete_page_here"),  
    path('delete_page_worldweatheronline', views.delete_page_worldweatheronline, name="delete_page_worldweatheronline"),
]
