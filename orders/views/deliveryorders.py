from collections import Counter, namedtuple

from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView
from django.urls import reverse_lazy, reverse

from shared.constants import ROLE_SUPPLIER, ROLE_ADMIN, ROLE_STAFF, ROLE_GUEST
from customers.models import Customer
from purchases.models import Product

from orders.forms import DeliveryOrderForm
from orders.mixins import BaseOrderView
from orders.models import Batch, DeliveryOrder, Allocation, Port, Distribution


class BaseOrderDetailView(BaseOrderView):
    """Base class for all delivery order detail views."""
    model = DeliveryOrder


class OrderDetailView(BaseOrderDetailView, DetailView):
    """Displays a detail of a single delivery order."""
    template_name = 'orders/order_detail.html'
    access_roles = '__all__'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role is None and not user.is_superuser:
            qs = DeliveryOrder.objects.none()
        elif user.role is not None and user.role.name == ROLE_SUPPLIER:
            qs = qs.filter(batch__supplier=user.supplier)
        return qs

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        distributed_buyers = self.object.distributions.values_list(
            'buyer', flat=True
        )
        buyer_choices = [c for c in customers if c.pk not in distributed_buyers]
        kwargs.update({'buyer_choices': buyer_choices,})
        return super().get_context_data(**kwargs)


class OrderCreateView(BaseOrderView, CreateView):
    """Creates new delivery order instances."""
    template_name = 'orders/order_create_form.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder
    object = None
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_batch(self):
        batch_pk = self.kwargs.get('batch_pk')
        return get_object_or_404(Batch, pk=batch_pk)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'batch': self.get_batch(),
            'port_list': Port.objects.all()
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        batch = self.get_batch()
        url = reverse('orders:batch-detail', args=[batch.pk])
        if self.object is not None:
            url = f'{url}?active_delivery_order={self.object.pk}'
        return url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.batch = self.get_batch()
        self.object.created_by = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class OrderUpdateView(BaseOrderDetailView, UpdateView):
    """Updates the a dilvery order instance."""
    template_name = 'orders/modals/order_form.html'
    form_class = DeliveryOrderForm
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'batch_list': Batch.objects.all(),
            'port_list': Port.objects.all()
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        url = reverse('orders:batch-detail', args=[self.object.batch.pk])
        url = f'{url}?active_delivery_order={self.object.pk}'
        return url

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class OrderDeleteView(BaseOrderDetailView, DeleteView):
    """Deletes a deliver order instance."""
    template_name = 'orders/modals/order_delete_form.html'
    access_roles = [ROLE_ADMIN]

    def get_success_url(self):
        delivery_order = self.get_object()
        batch_pk = delivery_order.batch.pk
        return reverse_lazy('orders:batch-detail', args=[batch_pk])
