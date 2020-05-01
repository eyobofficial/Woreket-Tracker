from django import forms
from django.forms import inlineformset_factory

from customers.models import Union

from .models import DeliveryOrder, Allocation, Distribution, UnionDistribution
from .fields import MoneyField


class DeliveryOrderForm(forms.ModelForm):
    """Model form for creating new deliveries."""
    quantity = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = DeliveryOrder
        fields = (
            'lc_number', 'batch', 'bill_of_loading',
            'quantity', 'port',  'vessel', 'arrival_date'
        )


class AllocationForm(forms.ModelForm):
    """Model form for creating new delivery order allocation."""
    quantity = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = Allocation
        fields = ('delivery_order', 'buyer', 'quantity')


class DistributionForm(forms.ModelForm):
    """Model form for creating new delivery order distribution."""

    class Meta:
        model = Distribution
        # fields = ('buyer', )
        fields = '__all__'


class UnionDistributionForm(forms.ModelForm):
    """Model form for creating new union distribution instance."""
    union = forms.ModelChoiceField(
        queryset=Union.objects.all(),
        empty_label=None,
        required=True
    )

    class Meta:
        model = UnionDistribution
        fields = ('union', 'quantity', 'shortage', 'over')


UnionDistributionFormSet = inlineformset_factory(
    Distribution,
    UnionDistribution,
    form=UnionDistributionForm,
    extra=0, min_num=1, validate_min=True, can_delete=True
)


class LetterDownloadForm(forms.Form):
    """Form for selecting a letter to download"""
    ALLOCATION_LETTER = 'ALLOCATION'
    RETENTION_LETTER = 'RETENTION'

    TYPE_CHOICES = (
        (ALLOCATION_LETTER, 'Delivery Order Allocation Letter'),
        (RETENTION_LETTER, '10% Payment Release Request Letter')
    )

    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)
