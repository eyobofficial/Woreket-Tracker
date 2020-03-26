from django import forms

from .fields import MoneyField
from .models import CreditLetter



class CreditLetterForm(forms.ModelForm):
    rate = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = CreditLetter
        fields = ('document_number', 'product', 'rate')
