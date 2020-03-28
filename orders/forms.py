from django import forms

from .models import DeliveryOrder, OrderAllocation

from .fields import MoneyField


class DeliveryOrderForm(forms.ModelForm):
    """Model form for creating new deliveries."""
    rate = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = DeliveryOrder
        fields = ('lc_number', 'vessel', 'supplier', 'product', 'rate')


class OrderAllocationForm(forms.ModelForm):
    """Model form for creating new delivery order allocation."""
    quantity = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = OrderAllocation
        fields = ('delivery_order', 'buyer', 'quantity')
