from django import forms
from .models import Restaurantsale

class RestaurantsaleForm(forms.ModelForm):
    class Meta:
        model = Restaurantsale
        fields = ('date', 'description', 'number_of_plates', 'price', 'payment_mode')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'payment_mode': forms.Select(choices=Restaurantsale.MODE_OF_PAYMENT_CHOICES)
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
