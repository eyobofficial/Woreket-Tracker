from django import forms

from .models import Allocation


class AllocationForm(forms.ModelForm):

    class Meta:
        model = Allocation
        fields = (
            'distribution_order',
            'region', 'location',
            'union', 'quantity'
        )
