from django.db import models

# Create your models here.
class City(models.Model):
    """This class represents the cities for which information is retrieved."""
    name = models.CharField(max_length=25)

    def __str__(self): #show the actual city name on the dashboard
        """show the actual city name on the dashboard"""
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        """When referring to the city objects in the admin panel, then use 'cities' instead of 'citys."""
        verbose_name_plural = 'cities'
