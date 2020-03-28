from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView
from django.urls import reverse_lazy, reverse

from shared.models import Product, Supplier, Customer

from .forms import DeliveryOrderForm, OrderAllocationForm
from .mixins import BaseOrderView
from .models import DeliveryOrder, OrderAllocation


class OpenOrderListView(BaseOrderView, ListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/open_orders_list.html'
    model = DeliveryOrder

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=DeliveryOrder.OPEN)


class OrderCreateView(BaseOrderView, CreateView):
    """Creates new delivery order instances."""
    template_name = 'orders/modals/order_form.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder
    object = None

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product_list': Product.objects.all(),
            'supplier_list': Supplier.objects.all()
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('orders:open-order-detail', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class OrderUpdateView(BaseOrderView, UpdateView):
    """Updates the a dilvery order instance."""
    template_name = 'orders/modals/order_form.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product_list': Product.objects.all(),
            'supplier_list': Supplier.objects.all()
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url


class OrderCloseView(BaseOrderView, UpdateView):
    """Closes a delivery order instance."""
    template_name = 'orders/modals/order_close.html'
    model = DeliveryOrder
    fields = ('status', )

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url


class OrderDetailView(BaseOrderView, DetailView):
    """Displays a detail of a single delivery order."""
    template_name = 'orders/open_order_detail.html'
    model = DeliveryOrder

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=DeliveryOrder.OPEN)


class AllocationCreateView(BaseOrderView, CreateView):
    """Creates an allocation for delivery order."""
    template_name = 'orders/modals/allocation_form.html'
    model = OrderAllocation
    form_class = OrderAllocationForm

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(DeliveryOrder,  pk=order_pk)
        allocated_buyers = order.order_allocations.values_list('buyer',
                                                                flat=True)
        buyer_choices = [c for c in customers if c.pk not in allocated_buyers]
        kwargs.update({
            'buyer_choices': buyer_choices,
            'order_pk': self.kwargs.get('pk')
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        order_pk = self.kwargs.get('pk')
        return reverse('orders:open-order-detail', args=[order_pk])

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect_url


class AllocationUpdateView(BaseOrderView, UpdateView):
    """Updates an allocation for delivery order."""
    template_name = 'orders/modals/allocation_form.html'
    model = OrderAllocation
    form_class = OrderAllocationForm

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order_pk = self.kwargs.get('pk')
        order = self.object.delivery_order
        allocated_buyers = order.order_allocations.values_list('buyer',
                                                               flat=True)
        buyer_choices = []
        for c in customers:
            if c.pk not in allocated_buyers or c == self.object.buyer:
                buyer_choices.append(c)

        kwargs.update({
            'buyer_choices': buyer_choices,
            'order_pk': self.object.delivery_order.pk
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse(
            'orders:open-order-detail',
            args=[self.object.delivery_order.pk]
        )

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect_url


class AllocationDeleteView(BaseOrderView, DeleteView):
    """Updates an allocation instance for delivery order."""
    template_name = 'orders/modals/allocation_delete_form.html'
    model = OrderAllocation

    def get_success_url(self):
        return reverse(
            'orders:open-order-detail',
            args=[self.object.delivery_order.pk]
        )

    def delete(self, request, *args, **kwargs):
        delivery_order = self.get_object().delivery_order
        redirect_url = super().delete(request, *args, **kwargs)
        delivery_order.touch(updated_by=request.user)
        return redirect_url
