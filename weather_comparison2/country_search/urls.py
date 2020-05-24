from django.urls import path
from . import views

app_name = "country_search"

urlpatterns = [
    path('', views.index, name='index'),  #the path for our index view
]
