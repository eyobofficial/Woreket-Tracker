from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from shared.models import Product, Supplier

from .forms import DeliveryOrderForm
from .mixins import BaseOrderView
from .models import DeliveryOrder


class OpenOrderListView(BaseOrderView, ListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/open_orders_list.html'
    model = DeliveryOrder

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=DeliveryOrder.OPEN)


class OrderCreateView(BaseOrderView, CreateView):
    """Creates new delivery order instances."""
    template_name = 'orders/modals/order_create.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder
    success_url = reverse_lazy('orders:open-orders-list')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product_list': Product.objects.all(),
            'supplier_list': Supplier.objects.all()
        })
        return super().get_context_data(**kwargs)
