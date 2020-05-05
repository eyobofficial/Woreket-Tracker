from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from shared.constants import ROLE_SUPPLIER, ROLE_ADMIN, ROLE_STAFF
from customers.models import Customer, Union, Location

from orders.forms import UnionDistributionFormSet, DistributionForm
from orders.mixins import BaseOrderView
from orders.models import DeliveryOrder, Distribution


class DistributionDetailView(BaseOrderView, DetailView):
    """Modal detail view for the distribution quantity calculation."""
    template_name = 'orders/modals/distributions/distribution_detail.html'
    model = Distribution
    access_roles = '__all__'


class BaseDistributionEditView(BaseOrderView):
    """Base abstract class for Distribution Create & Update views."""
    model = Distribution
    form_class = UnionDistributionFormSet
    prefix = 'formset'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def form_invalid(self, formset):
        response = super().form_invalid(formset)
        response.status_code = 400
        return response


class DistributionCreateView(BaseDistributionEditView, CreateView):
    """Creates a distribution report for delivery order."""
    template_name = 'orders/modals/distributions/distribution_create_form.html'

    def get_delivery_order(self):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(DeliveryOrder,  pk=order_pk)
        return order

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()
        order = self.get_delivery_order()
        distributed_buyers = order.distributions.values_list('buyer', flat=True)
        buyer_choices = [c for c in customers if c.pk not in distributed_buyers]

        try:
            buyer_pk = int(self.request.GET.get('buyer'))
            union_choices = Union.objects.filter(customer__pk=buyer_pk)
            location_choices = Location.objects.filter(customer__pk=buyer_pk)
        except TypeError:
            union_choices = Union.objects.all()
            location_choices = Location.objects.all()

        DistributionForm = modelform_factory(Distribution, fields=('buyer', ))
        kwargs.update({
            'buyer_choices': buyer_choices,
            'union_choices': union_choices,
            'location_choices': location_choices,
            'order': order,
            'formset': self.get_form(),
            'distribution_form': DistributionForm(self.request.POST or None)
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        order_pk = self.kwargs.get('pk')
        page_section = self.request.GET.get('section')
        return reverse('orders:order-detail', args=[order_pk])

    def form_valid(self, formset):
        context = self.get_context_data()
        distribution_form = context['distribution_form']
        if distribution_form.is_valid():
            self.object = distribution_form.save(commit=False)
            self.object.delivery_order = self.get_delivery_order()
            self.object.created_by = self.request.user
            self.object.save()

            formset.instance = self.object
            self.object.delivery_order.touch(updated_by=self.request.user)
            return super().form_valid(formset)
        return super().form_invalid(formset)


class DistributionUpdateView(BaseDistributionEditView, UpdateView):
    """Updates a distribution for delivery order."""
    template_name = 'orders/modals/distributions/distribution_update_form.html'

    def get_context_data(self, **kwargs):
        union_choices = Union.objects.filter(customer=self.object.buyer)
        location_choices = Location.objects.filter(customer=self.object.buyer)
        DistributionForm = modelform_factory(Distribution, fields=('buyer', ))
        kwargs.update({
            'union_choices': union_choices,
            'location_choices': location_choices,
            'order': self.object.delivery_order,
            'formset': self.get_form(),
            'distribution_form': DistributionForm(
                self.request.POST or None,
                instance=self.object.buyer
            )
        })
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        distribution_pk = self.kwargs.get('pk')
        distribution = get_object_or_404(Distribution, pk=distribution_pk)
        order_pk = distribution.delivery_order.pk
        return reverse('orders:order-detail', args=[order_pk])

    def form_valid(self, formset):
        redirect_url = super().form_valid(formset)
        self.object = formset.instance
        self.object.delivery_order.touch(updated_by=self.request.user)
        return redirect_url


class DistributionDeleteView(BaseOrderView, DeleteView):
    """Deletes a distribution instance for delivery order."""
    template_name = 'orders/modals/distributions/distribution_delete_form.html'
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
        return url

    def delete(self, request, *args, **kwargs):
        delivery_order = self.get_object().delivery_order
        redirect_url = super().delete(request, *args, **kwargs)
        delivery_order.touch(updated_by=request.user)
        return redirect_url
