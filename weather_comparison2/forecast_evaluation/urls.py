from django.urls import path
from . import views

app_name = "forecast_evaluation"
urlpatterns = [
    path('', views.index, name="index"),  #the path for our index view
    path('delete_page', views.delete_page, name="delete_page"),
    path('city_page', views.city_page, name="city_page"), 
    path('forecast_evaluation_bludenz', views.forecast_evaluation_bludenz, name="forecast_evaluation_bludenz"),
    path('forecast_evaluation_vaduz', views.forecast_evaluation_vaduz, name="forecast_evaluation_vaduz"),
    path('forecast_evaluation_zurich', views.forecast_evaluation_zurich, name="forecast_evaluation_zurich"),
    path('forecast_evaluation_oslo', views.forecast_evaluation_oslo, name="forecast_evaluation_oslo"),
    path('forecast_evaluation_madrid', views.forecast_evaluation_madrid, name="forecast_evaluation_madrid"),
    path('forecast_evaluation_paris', views.forecast_evaluation_paris, name="forecast_evaluation_paris"),
]
