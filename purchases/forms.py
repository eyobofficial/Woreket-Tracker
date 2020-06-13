from django import forms
from django_countries.fields import CountryField

from phonenumber_field.formfields import PhoneNumberField

from shared.fields import FormattedNumberField
from .models import Supplier


class SupplierForm(forms.ModelForm):
    """Model for creating new supplier."""
    phone_number = PhoneNumberField(
        required=False,
        empty_value=None,
        error_messages={
            'invalid': 'Enter a valid mobile phone number.'
        }
    )
    fax_number = PhoneNumberField(
        required=False,
        empty_value=None,
        error_messages={
            'invalid': 'Enter a valid fax phone number.'
        }
    )
    country = CountryField(blank_label='Choose country').formfield()

    class Meta:
        model = Supplier
        fields = (
            'name', 'short_name', 'email',
            'phone_number', 'fax_number', 'city', 'country'
        )
