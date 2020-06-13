from collections import Counter, namedtuple

from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView
from django.urls import reverse_lazy, reverse

from shared.constants import ROLE_SUPPLIER, ROLE_ADMIN, ROLE_STAFF
from customers.models import Customer
from purchases.models import Product

from orders.forms import DeliveryOrderForm
from orders.mixins import BaseOrderView
from orders.models import Batch, DeliveryOrder, Allocation, Port, Distribution


class BaseOrderListView(BaseOrderView, ListView):
    """Abstract base class for open & closed order list views."""
    model = DeliveryOrder
    queryset = DeliveryOrder.objects.all()
    paginate_by = 10
    status = None

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(batch__status=self.status)

        user = self.request.user
        batch_pk = self.request.GET.get('batch', '')
        product_pk = self.request.GET.get('product', '')
        search_query = self.request.GET.get('search')

        if user.role and user.role.name == ROLE_SUPPLIER:
            qs = qs.filter(batch__supplier=user.supplier)

        if product_pk:
            qs = qs.filter(batch__product__pk=product_pk).distinct()

        if batch_pk:
            qs = qs.filter(batch__pk=batch_pk)

        if search_query is not None:
            search_query = search_query.strip()
            qs = self.get_search_result(search_query)
        return qs

    def get_context_data(self, **kwargs):
        user = self.request.user
        # Build product menu
        ProductMenu = namedtuple('ProductMenu', ['product', 'count'])
        products = Product.objects.filter(
            batches__status=self.status
        )
        if user.role and user.role.name == ROLE_SUPPLIER:
            products = products.filter(batches__supplier=user.supplier)

        products = Counter(products)
        products = [ProductMenu(p, c) for p, c in products.items()]

        # Selected Product
        product_pk = self.request.GET.get('product', '')
        if product_pk:
            selected_product = Product.objects.filter(pk=product_pk).first()
        else:
            selected_product = None

        # Build Batch Menu
        BatchMenu = namedtuple('BatchMenu', ['batch', 'count'])
        batches = Batch.objects.filter(
            status=self.status, delivery_orders__isnull=False
        )
        if user.role and user.role.name == ROLE_SUPPLIER:
            batches = batches.filter(supplier=user.supplier)

        batches = Counter(batches)
        batches = [BatchMenu(b, c) for b, c in batches.items()]

        # Selected Batch
        batch_pk = self.request.GET.get('batch', '')
        if batch_pk:
            selected_batch = Batch.objects.filter(pk=batch_pk).first()
        else:
            selected_batch = None

        kwargs.update({
            'order_count': self.queryset.count(),
            'search_query': self.request.GET.get('search', '').strip(),

            'product_menu': products,
            'selected_product': selected_product,

            'batch_menu': batches,
            'selected_batch': selected_batch
        })
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns a delivery order queryset using search query."""
        return self.queryset.filter(vessel__istartswith=query)


class OpenOrderListView(BaseOrderListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/open_orders_list.html'
    status = Batch.OPEN
    access_roles = '__all__'


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


# class BatchSummaryView(BaseOrderView, DetailView):
#     """A popup modal for batch summary page."""
#     template_name = 'orders/modals/batch_summary.html'
#     model = Batch
#     access_roles = '__all__'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.exclude(is_deleted=True)
#         return qs


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
    success_url = reverse_lazy('orders:closed-orders-list')
    access_roles = [ROLE_ADMIN]

    def get_success_url(self):
        delivery_order = self.get_object()
        batch_pk = delivery_order.batch.pk
        return reverse_lazy('orders:batch-detail', args=[batch_pk])
