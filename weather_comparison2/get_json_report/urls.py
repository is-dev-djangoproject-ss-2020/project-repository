from django.urls import path
from . import views

app_name = "get_json_report"
urlpatterns = [
    path('openweathermap', views.openweathermap, name="openweathermap"),  #the path for our index view
    path('weatherbit', views.weatherbit, name="weatherbit"),
    path('here', views.here, name="here"),
    path('worldweatheronline', views.worldweatheronline, name="worldweatheronline"),
    path('complete', views.complete, name="complete"),
    path('empty', views.empty, name="empty"), 
]
