from collections import Counter, namedtuple

from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView, FormView
from django.views.generic.detail import BaseDetailView
from django.urls import reverse_lazy, reverse

from shared.constants import ROLE_SUPPLIER, ROLE_ADMIN, ROLE_STAFF
from shared.models import Customer, Batch, Product

from .forms import DeliveryOrderForm, AllocationForm, LetterDownloadForm, \
    DistributionForm
from .mixins import BaseOrderView
from .models import DeliveryOrder, Allocation, Port, Distribution
from .letters.allocationletter import AllocationLetter


class BaseOrderListView(BaseOrderView, ListView):
    """Abstract base class for open & closed order list views."""
    model = DeliveryOrder
    paginate_by = 10
    status = None

    def get_queryset(self):
        qs = super().get_queryset()

        user = self.request.user
        lc_number = self.request.GET.get('lc')
        batch_pk = self.request.GET.get('batch')
        product_pk = self.request.GET.get('product')
        search_query = self.request.GET.get('search')

        if user.role and user.role.name == ROLE_SUPPLIER:
            qs = qs.filter(batch__supplier=user.supplier)

        if lc_number is not None:
            qs = qs.filter(lc_number=lc_number)

        if product_pk is not None:
            qs = qs.filter(batch__product__pk=product_pk).distinct()

        if batch_pk is not None:
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
            batches__delivery_orders__status=self.status
        )
        if user.role and user.role.name == ROLE_SUPPLIER:
            products = products.filter(batches__supplier=user.supplier)

        products = Counter(products)
        products = [ProductMenu(p, c) for p, c in products.items()]

        # Selected Product
        product_pk = self.request.GET.get('product')
        selected_product = Product.objects.filter(pk=product_pk).first()

        # Build Batch Menu
        BatchMenu = namedtuple('BatchMenu', ['batch', 'count'])
        batches = Batch.objects.filter(
            delivery_orders__status=self.status,
            delivery_orders__isnull=False
        )
        if user.role and user.role.name == ROLE_SUPPLIER:
            batches = batches.filter(supplier=user.supplier)

        batches = Counter(batches)
        batches = [BatchMenu(b, c) for b, c in batches.items()]

        # Selected Batch
        batch_pk = self.request.GET.get('batch')
        selected_batch = Batch.objects.filter(pk=batch_pk).first()

        kwargs.update({
            'order_count': self.queryset.count(),
            'search_query': self.request.GET.get('search', '').strip(),

            'lc_menu': self.get_lc_list(),
            'selected_lc': self.request.GET.get('lc'),

            'product_menu': products,
            'selected_product': selected_product,

            'batch_menu': batches,
            'selected_batch': selected_batch
        })
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns a delivery order queryset using search query."""
        search_qs = self.queryset.filter(
            Q(vessel__icontains=query) |
            Q(lc_number__icontains=query) |
            Q(batch__product__name__icontains=query)
        )
        return search_qs

    def get_lc_list(self):
        """Returns LC numbers for open delivery orders.

        Args:
            status (constant): status of the delivery orders to return
        Return:
            lc numbers: list of tuple of lc numbers with their count
        Raise:
            TypeError: when a status argument is missing
        """
        LCNumber = namedtuple('LCNumber', ['lc_number', 'count'])
        user = self.request.user
        qs = DeliveryOrder.objects.filter(status=self.status)

        if user.role and user.role.name == ROLE_SUPPLIER:
            qs = qs.filter(batch__supplier=user.supplier)

        qs = qs.values_list('lc_number', flat=True)
        counter = Counter(qs)
        return [LCNumber(l, c) for l, c in counter.items()]


class OpenOrderListView(BaseOrderListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/open_orders_list.html'
    queryset = DeliveryOrder.objects.filter(status=DeliveryOrder.OPEN)
    status = DeliveryOrder.OPEN
    access_roles = '__all__'


class ClosedOrderListView(BaseOrderListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/closed_orders_list.html'
    queryset = DeliveryOrder.objects.filter(status=DeliveryOrder.CLOSED)
    status = DeliveryOrder.CLOSED
    access_roles = '__all__'


class OrderDetailView(BaseOrderView, DetailView):
    """Displays a detail of a single delivery order."""
    template_name = 'orders/order_detail.html'
    model = DeliveryOrder
    access_roles = '__all__'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role.name == ROLE_SUPPLIER and user.supplier:
            qs = qs.filter(batch__supplier=user.supplier)
        return qs

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        distributed_buyers = self.object.distributions.values_list(
            'buyer', flat=True
        )
        buyer_choices = [c for c in customers if c.pk not in distributed_buyers]

        # Build graph data
        regions = customers.order_by('code').values_list('code', flat=True)
        graph = dict()
        graph['regions'] = list(regions)
        graph['allocations'] = []
        graph['distributions'] = []

        for region in graph['regions']:
            allocation = Allocation.objects.filter(
                delivery_order=self.object,
                buyer__code=region
            ).first()
            if allocation is not None:
                graph['allocations'].append(allocation.quantity)
            else:
                graph['allocations'].append(0)

            distribution = Distribution.objects.filter(
                delivery_order=self.object,
                buyer__code=region
            ).first()

            if distribution is not None:
                graph['distributions'].append(distribution.quantity)
            else:
                graph['distributions'].append(0)

        kwargs.update({
            'buyer_choices': buyer_choices,
            'graph': graph
        })
        return super().get_context_data(**kwargs)


class BatchSummaryView(BaseOrderView, DetailView):
    """A popup modal for batch summary page."""
    template_name = 'orders/modals/batch_summary.html'
    model = Batch
    access_roles = '__all__'


class BillOfLoadingSummary(BaseOrderView, DetailView):
    """A popup modal for bill of loading summary page."""
    template_name = 'orders/modals/bill_of_loading_summary.html'
    model = DeliveryOrder
    access_roles = '__all__'


class OrderCreateView(BaseOrderView, CreateView):
    """Creates new delivery order instances."""
    template_name = 'orders/modals/order_form.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder
    object = None
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'batch_list': Batch.objects.all(),
            'port_list': Port.objects.all()
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('orders:order-detail', args=[self.object.pk])

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
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'batch_list': Batch.objects.all(),
            'port_list': Port.objects.all()
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
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url


class OrderReopenView(BaseOrderView, UpdateView):
    """Opens a delivery order instance."""
    template_name = 'orders/modals/order_open.html'
    model = DeliveryOrder
    fields = ('status', )
    access_roles = [ROLE_ADMIN]

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url


class OrderDeleteView(BaseOrderView, DeleteView):
    """Deletes a deliver order instance."""
    template_name = 'orders/modals/order_delete_form.html'
    model = DeliveryOrder
    success_url = reverse_lazy('orders:closed-orders-list')
    access_roles = [ROLE_ADMIN]


class AllocationCreateView(BaseOrderView, CreateView):
    """Creates an allocation for delivery order."""
    template_name = 'orders/modals/allocation_form.html'
    model = Allocation
    form_class = AllocationForm
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(DeliveryOrder,  pk=order_pk)
        allocated_buyers = order.allocations.values_list('buyer', flat=True)
        buyer_choices = [c for c in customers if c.pk not in allocated_buyers]
        kwargs.update({
            'buyer_choices': buyer_choices,
            'order': order
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        order_pk = self.kwargs.get('pk')
        page_section = self.request.GET.get('section')
        url = reverse('orders:order-detail', args=[order_pk])
        if page_section is not None:
            url = f'{url}#{page_section}'
        return url

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect_url


class AllocationUpdateView(BaseOrderView, UpdateView):
    """Updates an allocation for delivery order."""
    template_name = 'orders/modals/allocation_form.html'
    model = Allocation
    form_class = AllocationForm
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order_pk = self.kwargs.get('pk')
        order = self.object.delivery_order
        allocated_buyers = order.allocations.values_list('buyer', flat=True)
        buyer_choices = []
        for c in customers:
            if c.pk not in allocated_buyers or c == self.object.buyer:
                buyer_choices.append(c)

        kwargs.update({
            'buyer_choices': buyer_choices,
            'order': self.object.delivery_order
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        page_section = self.request.GET.get('section')
        url = reverse(
            'orders:order-detail',
            args=[self.object.delivery_order.pk]
        )
        if page_section:
            url = f'{url}#{page_section}'
        return url

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect_url


class AllocationDeleteView(BaseOrderView, DeleteView):
    """Deletes an allocation instance for delivery order."""
    template_name = 'orders/modals/allocation_delete_form.html'
    model = Allocation
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_success_url(self):
        page_section = self.request.GET.get('section')
        url = reverse(
            'orders:order-detail',
            args=[self.object.delivery_order.pk]
        )
        if page_section is not None:
            url = f'{url}#{page_section}'
        return url

    def delete(self, request, *args, **kwargs):
        delivery_order = self.get_object().delivery_order
        redirect_url = super().delete(request, *args, **kwargs)
        delivery_order.touch(updated_by=request.user)
        return redirect_url


class LetterFormView(BaseOrderView, FormView):
    """Form view to select a letter to download."""
    template_name = 'orders/modals/letter_form.html'
    form_class = LetterDownloadForm
    access_roles = '__all__'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        kwargs['object'] = get_object_or_404(DeliveryOrder, pk=pk)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        letter_type = form.cleaned_data['type']
        pk = self.kwargs.get('pk')
        if letter_type == self.form_class.ALLOCATION_LETTER:
            view_url = reverse('orders:order-allocation-letter', args=[pk])
            return redirect(view_url)
        return


class AllocationLetterView(BaseOrderView, BaseDetailView):
    """Generates delivery order allocation letter."""
    model = DeliveryOrder
    access_roles = '__all__'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        letter = AllocationLetter(self.object)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename=allocation.docx'
        letter.generate(response)
        return response


class DistributionDetailView(BaseOrderView, DetailView):
    """Modal detail view for the distribution quantity calculation."""
    template_name = 'orders/modals/distribution_detail.html'
    model = Distribution
    access_roles = '__all__'


class DistributionCreateView(BaseOrderView, CreateView):
    """Creates a distribution repoort for delivery order."""
    template_name = 'orders/modals/distribution_form.html'
    model = Distribution
    form_class = DistributionForm
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(DeliveryOrder,  pk=order_pk)
        distributed_buyers = order.distributions.values_list('buyer', flat=True)
        buyer_choices = [c for c in customers if c.pk not in distributed_buyers]
        kwargs.update({
            'buyer_choices': buyer_choices,
            'order': order
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        order_pk = self.kwargs.get('pk')
        page_section = self.request.GET.get('section')
        url = reverse('orders:order-detail', args=[order_pk])
        if page_section is not None:
            url = f'{url}#{page_section}'
        return url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect(self.get_success_url())


class DistributionUpdateView(BaseOrderView, UpdateView):
    """Updates a distribution for delivery order."""
    template_name = 'orders/modals/distribution_form.html'
    model = Distribution
    form_class = DistributionForm
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order_pk = self.kwargs.get('pk')
        order = self.object.delivery_order
        distributed_buyers = order.distributions.values_list('buyer', flat=True)
        buyer_choices = []
        for c in customers:
            if c.pk not in distributed_buyers or c == self.object.buyer:
                buyer_choices.append(c)
        page_section = self.request.GET.get('section')
        kwargs.update({
            'buyer_choices': buyer_choices,
            'order': order,
            'section': page_section
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        page_section = self.request.GET.get('section')
        url = reverse(
            'orders:order-detail',
            args=[self.object.delivery_order.pk]
        )
        if page_section is not None:
            url = f'{url}#{page_section}'
        return url

    def form_valid(self, form):
        self.object = form.save(commit=True)
        self.object.updated_by = self.request.user
        self.object.save()
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect(self.get_success_url())


class DistributionDeleteView(BaseOrderView, DeleteView):
    """Deletes a distribution instance for delivery order."""
    template_name = 'orders/modals/distribution_delete_form.html'
    model = Distribution
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        page_section = self.request.GET.get('section')
        kwargs.update(section=page_section)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        page_section = self.request.GET.get('section')
        url = reverse(
            'orders:order-detail',
            args=[self.object.delivery_order.pk]
        )
        if page_section is not None:
            url = f'{url}#{page_section}'
        return url

    def delete(self, request, *args, **kwargs):
        delivery_order = self.get_object().delivery_order
        redirect_url = super().delete(request, *args, **kwargs)
        delivery_order.touch(updated_by=request.user)
        return redirect_url
