from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, \
    DetailView, FormView
from django.views.generic.detail import BaseDetailView
from django.urls import reverse

from shared.constants import ROLE_SUPPLIER, ROLE_ADMIN, ROLE_STAFF
from customers.models import Customer, Union, Location

from orders.forms import AllocationForm, LetterDownloadForm, \
    UnionAllocationFormSet
from orders.mixins import BaseOrderView
from orders.models import DeliveryOrder, Allocation
from orders.letters.allocationletter import AllocationLetter


class AllocationDetailView(BaseOrderView, DetailView):
    """Modal detail view for the allocation quantity calculation."""
    template_name = 'orders/modals/allocations/allocation_detail.html'
    model = Allocation
    access_roles = '__all__'


class BaseAllocationEditView(BaseOrderView):
    """Abstract base class for allocation create & update people."""
    model = Allocation
    form_class = UnionAllocationFormSet
    prefix = 'formset'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def form_invalid(self, formset):
        response = super().form_invalid(formset)
        response.status_code = 400
        return response


class AllocationCreateView(BaseAllocationEditView, CreateView):
    """Creates an allocation for delivery order."""
    template_name = 'orders/modals/allocations/allocation_create_form.html'

    def get_delivery_order(self):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(DeliveryOrder,  pk=order_pk)
        return order

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order = self.get_delivery_order()
        allocated_buyers = order.allocations.values_list('buyer', flat=True)
        buyer_choices = [c for c in customers if c.pk not in allocated_buyers]

        try:
            buyer_pk = int(self.request.GET.get('buyer'))
            union_choices = Union.objects.filter(customer__pk=buyer_pk)
            location_choices = Location.objects.filter(customer__pk=buyer_pk)
        except TypeError:
            union_choices = Union.objects.all()
            location_choices = Location.objects.all()

        AllocationForm = modelform_factory(Allocation, fields=('buyer', ))
        kwargs.update({
            'buyer_choices': buyer_choices,
            'union_choices': union_choices,
            'location_choices': location_choices,
            'order': order,
            'formset': self.get_form(),
            'allocation_form': AllocationForm(self.request.POST or None)
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        order_pk = self.kwargs.get('pk')
        return reverse('orders:order-detail', args=[order_pk])

    def form_valid(self, formset):
        context = self.get_context_data()
        allocation_form = context['allocation_form']
        if allocation_form.is_valid():
            self.object = allocation_form.save(commit=False)
            self.object.delivery_order = self.get_delivery_order()
            self.object.created_by = self.request.user
            self.object.save()

            formset.instance = self.object
            self.object.delivery_order.touch(updated_by=self.request.user)
            return super().form_valid(formset)
        return super().form_invalid(formset)


class AllocationUpdateView(BaseAllocationEditView, UpdateView):
    """Updates an allocation for delivery order."""
    template_name = 'orders/modals/allocations/allocation_update_form.html'

    def get_context_data(self, **kwargs):
        union_choices = Union.objects.filter(customer=self.object.buyer)
        location_choices = Location.objects.filter(customer=self.object.buyer)
        AllocationForm = modelform_factory(Allocation, fields=('buyer', ))
        kwargs.update({
            'union_choices': union_choices,
            'location_choices': location_choices,
            'order': self.object.delivery_order,
            'formset': self.get_form(),
            'allocation_form': AllocationForm(
                self.request.POST or None,
                instance=self.object.buyer
            )
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        allocation_pk = self.kwargs.get('pk')
        allocation = get_object_or_404(Allocation, pk=allocation_pk)
        order_pk = allocation.delivery_order.pk
        return reverse('orders:order-detail', args=[order_pk])

    def form_valid(self, formset):
        redirect_url = super().form_valid(formset)
        self.object = formset.instance
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect_url


class AllocationDeleteView(BaseOrderView, DeleteView):
    """Deletes an allocation instance for delivery order."""
    template_name = 'orders/modals/allocations/allocation_delete_form.html'
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
