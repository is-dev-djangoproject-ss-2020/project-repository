from django.urls import path
from . import views

app_name = "weather_api1"
urlpatterns = [
    path('', views.index, name="index"),  #the path for our index view
]
