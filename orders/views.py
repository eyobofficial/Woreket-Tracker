from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView, FormView
from django.views.generic.detail import BaseDetailView
from django.urls import reverse_lazy, reverse

from shared.models import Customer, Batch

from .forms import DeliveryOrderForm, AllocationForm, LetterDownloadForm, \
    DistributionForm
from .mixins import BaseOrderView
from .models import DeliveryOrder, Allocation, Port, Distribution
from .letters.allocationletter import AllocationLetter


class OpenOrderListView(BaseOrderView, ListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/open_orders_list.html'
    model = DeliveryOrder

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=DeliveryOrder.OPEN)


class ClosedOrderListView(BaseOrderView, ListView):
    """Lists all delivery orders with open status."""
    template_name = 'orders/closed_orders_list.html'
    model = DeliveryOrder

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=DeliveryOrder.CLOSED)


class OrderDetailView(BaseOrderView, DetailView):
    """Displays a detail of a single delivery order."""
    template_name = 'orders/order_detail.html'
    model = DeliveryOrder

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


class OrderCreateView(BaseOrderView, CreateView):
    """Creates new delivery order instances."""
    template_name = 'orders/modals/order_form.html'
    form_class = DeliveryOrderForm
    model = DeliveryOrder
    object = None

    def get_context_data(self, **kwargs):
        kwargs.update({
            'batch_list': Batch.objects.all(),
            'port_list': Port.objects.all()
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

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url


class OrderReopenView(BaseOrderView, UpdateView):
    """Opens a delivery order instance."""
    template_name = 'orders/modals/order_open.html'
    model = DeliveryOrder
    fields = ('status', )

    def form_valid(self, form):
        redirect_url = super().form_valid(form)
        self.object.touch(updated_by=self.request.user)
        return redirect_url


class OrderDeleteView(BaseOrderView, DeleteView):
    """Deletes a deliver order instance."""
    template_name = 'orders/modals/order_delete_form.html'
    model = DeliveryOrder
    success_url = reverse_lazy('orders:closed-orders-list')


class AllocationCreateView(BaseOrderView, CreateView):
    """Creates an allocation for delivery order."""
    template_name = 'orders/modals/allocation_form.html'
    model = Allocation
    form_class = AllocationForm

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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        letter = AllocationLetter(self.object)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename=do-letter.docx'
        letter.generate(response)
        return response


class DistributionDetailView(BaseOrderView, DetailView):
    """Modal detail view for the distribution quantity calculation."""
    template_name = 'orders/modals/distribution_detail.html'
    model = Distribution


class DistributionCreateView(BaseOrderView, CreateView):
    """Creates a distribution repoort for delivery order."""
    template_name = 'orders/modals/distribution_form.html'
    model = Distribution
    form_class = DistributionForm

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
