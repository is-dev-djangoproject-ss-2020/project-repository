from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    """This form represents the cities how the input information from the webpage is handled."""
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder
