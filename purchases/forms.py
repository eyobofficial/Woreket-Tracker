from django import forms
from django_countries.fields import CountryField

from shared.fields import FormattedNumberField

from .models import Supplier


class SupplierForm(forms.ModelForm):
    """Model for creating new supplier."""
    country = CountryField(blank_label='Choose country').formfield()

    class Meta:
        model = Supplier
        fields = ('name', 'short_name', 'email', 'city', 'country')
