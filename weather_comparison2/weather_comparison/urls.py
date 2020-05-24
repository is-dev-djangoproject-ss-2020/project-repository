"""weather_comparison URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('current_weather/', include('weather_api1.urls')),
    path('weather_forecast/', include('weather_api2.urls')),
    path('weather_cities/', include('weather_cities.urls')),
    path('weather_cities_forecast/', include('weather_cities_forecast.urls')),
    path('country_search/', include('country_search.urls')),
    path('home/', include('home.urls')),
    path('get_json_report/', include('get_json_report.urls')),
]
