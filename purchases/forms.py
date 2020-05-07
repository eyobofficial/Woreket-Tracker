from django import forms

from shared.fields import FormattedNumberField

from .models import Batch


class BatchForm(forms.ModelForm):
    """Model for creating new batch instance."""
    quantity = FormattedNumberField(max_digits=10, decimal_places=2)
    rate = FormattedNumberField(max_digits=10, decimal_places=2)

    class Meta:
        model = Batch
        fields = ('name', 'product', 'supplier', 'quantity', 'rate', 'year')
