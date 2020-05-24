from django.urls import path
from . import views

app_name = 'weather_api2'
urlpatterns = [
    path('', views.index, name='index'),  #the path for our index view
    path('weatherbit', views.weatherbit, name='weatherbit'),  #the path for our index view
    path('here', views.here, name='here'),  #the path for our index view
    path('worldweatheronline', views.worldweatheronline, name='worldweatheronline'),  #the path for our index view
    path('all_on_one_page', views.all_on_one_page, name='all_on_one_page'),  #the path for our index view
]
