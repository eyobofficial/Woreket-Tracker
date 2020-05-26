from django import forms
from django_countries.fields import CountryField

from shared.fields import FormattedNumberField

from .models import Batch, Supplier


class BatchForm(forms.ModelForm):
    """Model for creating new batch instance."""
    quantity = FormattedNumberField(max_digits=20, decimal_places=4)
    rate = FormattedNumberField(max_digits=12, decimal_places=4)

    class Meta:
        model = Batch
        fields = ('name', 'product', 'supplier', 'quantity', 'rate', 'year')


class SupplierForm(forms.ModelForm):
    """Model for creating new supplier."""
    country = CountryField(blank_label='Choose country').formfield()

    class Meta:
        model = Supplier
        fields = ('name', 'short_name', 'email', 'city', 'country')
