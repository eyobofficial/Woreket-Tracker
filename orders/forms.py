from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from shared.fields import FormattedNumberField
from customers.models import Union, Location

from .models import Batch, DeliveryOrder, Allocation, Distribution, \
    UnionDistribution, UnionAllocation


class BatchForm(forms.ModelForm):
    """Model for creating new batch instance."""
    quantity = FormattedNumberField(max_digits=20, decimal_places=4)
    rate = FormattedNumberField(max_digits=12, decimal_places=4)

    class Meta:
        model = Batch
        fields = ('name', 'lc_number', 'product',
                  'supplier', 'quantity', 'rate', 'year')


class DeliveryOrderForm(forms.ModelForm):
    """Model form for creating new deliveries."""
    class Meta:
        model = DeliveryOrder
        fields = (
            'bill_of_loading', 'port',  'vessel', 'arrival_date'
        )


class AllocationForm(forms.ModelForm):
    """Model form for creating new delivery order allocation."""
    quantity = FormattedNumberField(max_digits=20, decimal_places=4)

    class Meta:
        model = Allocation
        fields = ('buyer', )


class UnionAllocationForm(forms.ModelForm):
    """Model form for creating new union allocation instance."""
    union = forms.ModelChoiceField(
        queryset=Union.objects.all(),
        empty_label=None,
        required=True
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label=None,
        required=True
    )
    quantity = FormattedNumberField(max_digits=20, decimal_places=4)

    class Meta:
        model = UnionAllocation
        fields = ('union', 'location', 'quantity')


class BaseUnionAllocationFormSet(BaseInlineFormSet):
    def clean(self):
        """Remove validation for forms to be deleted."""
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue


UnionAllocationFormSet = inlineformset_factory(
    Allocation,
    UnionAllocation,
    form=UnionAllocationForm,
    formset=BaseUnionAllocationFormSet,
    extra=0, min_num=1,
    validate_min=True, can_delete=True
)


class DistributionForm(forms.ModelForm):
    """Model form for creating new delivery order distribution."""

    class Meta:
        model = Distribution
        fields = ('buyer', )


class UnionDistributionForm(forms.ModelForm):
    """Model form for creating new union distribution instance."""
    union = forms.ModelChoiceField(
        queryset=Union.objects.all(),
        empty_label=None,
        required=True
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label=None,
        required=True
    )
    quantity = FormattedNumberField(max_digits=20, decimal_places=4)
    shortage = FormattedNumberField(max_digits=20, decimal_places=4)
    over = FormattedNumberField(max_digits=20, decimal_places=4)

    class Meta:
        model = UnionDistribution
        fields = ('union', 'location', 'quantity', 'shortage', 'over')


class BaseUnionDistributionFormSet(BaseInlineFormSet):
    def clean(self):
        """Remove validation for forms to be deleted."""
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue


UnionDistributionFormSet = inlineformset_factory(
    Distribution,
    UnionDistribution,
    form=UnionDistributionForm,
    formset=BaseUnionDistributionFormSet,
    extra=0, min_num=1,
    validate_min=True, can_delete=True
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
