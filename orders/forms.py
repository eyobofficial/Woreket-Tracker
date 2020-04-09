from django import forms

from .models import DeliveryOrder, Allocation, Distribution

from .fields import MoneyField


class DeliveryOrderForm(forms.ModelForm):
    """Model form for creating new deliveries."""

    class Meta:
        model = DeliveryOrder
        fields = (
            'lc_number', 'batch', 'bill_of_loading',
            'port',  'vessel', 'arrival_date'
        )


class AllocationForm(forms.ModelForm):
    """Model form for creating new delivery order allocation."""
    quantity = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = Allocation
        fields = ('delivery_order', 'buyer', 'quantity')


class DistributionForm(forms.ModelForm):
    """Model form for creating new delivery order distribution."""
    quantity = MoneyField(max_digits=10, decimal_places=2)
    shortage = MoneyField(
        max_digits=10,
        decimal_places=2,
        required=False
    )
    over = MoneyField(
        max_digits=10,
        decimal_places=2,
        required=False
    )

    class Meta:
        model = Distribution
        fields = ('delivery_order', 'buyer', 'quantity', 'shortage', 'over')


class LetterDownloadForm(forms.Form):
    """Form for selecting a letter to download"""
    ALLOCATION_LETTER = 'ALLOCATION'
    RETENTION_LETTER = 'RETENTION'

    TYPE_CHOICES = (
        (ALLOCATION_LETTER, 'Delivery Order Allocation Letter'),
        (RETENTION_LETTER, '10% Payment Release Request Letter')
    )

    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)
