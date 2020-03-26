from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from shared.models import Product, Supplier

from .forms import DeliveryOrderForm
from .mixins import BaseOrderView
from .models import DeliveryOrder


class DeliveryOrderOverview(BaseOrderView, TemplateView):
    template_name = 'orders/overview.html'


class DeliveryOrderCreateView(BaseOrderView, CreateView):
    template_name = 'orders/modals/do_create.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder
    success_url = reverse_lazy('orders:overview')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product_list': Product.objects.all(),
            'supplier_list': Supplier.objects.all()
        })
        return super().get_context_data(**kwargs)
