from django.contrib import admin
from .models import City
from .models import Forecast_1_OWM
from .models import Forecast_1_Weatherbit
from .models import Forecast_1_here
from .models import Forecast_1_WWO

# Register your models here.
admin.site.register(Forecast_1_OWM)
admin.site.register(Forecast_1_Weatherbit)
admin.site.register(Forecast_1_here)
admin.site.register(Forecast_1_WWO)
admin.site.register(City)
