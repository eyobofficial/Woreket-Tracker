from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF

from .mixins import BaseCustomersView
from .models import Customer, Union


class UnionListView(BaseCustomersView, ListView):
    """List view of registered unions."""
    template_name = 'customers/union_list.html'
    model = Union
    paginate_by = 10
    page_name = 'unions'
    queryset = Union.objects.all()
    access_roles = [ROLE_STAFF, ROLE_MANAGEMENT, ROLE_ADMIN]

    def get_queryset(self):
        qs = super().get_queryset()
        region_pk = self.request.GET.get('region')
        search_query = self.request.GET.get('search')

        if region_pk is not None:
            qs = qs.filter(customer__pk=region_pk)

        if search_query is not None:
            qs = self.get_search_result(search_query)

        return qs

    def get_context_data(self, **kwargs):
        kwargs['customer_list'] = Customer.objects.all()
        kwargs['selected_region'] = self.request.GET.get('region')
        kwargs['union_count'] = self.queryset.count()
        kwargs['search_query'] = self.request.GET.get('search', '').strip()
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns matching unions using search query."""
        search_qs = self.queryset.filter(
            Q(name__icontains=query) |
            Q(customer__region__icontains=query)
        )
        return search_qs


class UnionCreateView(BaseCustomersView, SuccessMessageMixin, CreateView):
    """Create view for creating new unions."""
    template_name = 'customers/modals/unions/union_form.html'
    model = Union
    fields = ('name', 'customer')
    success_url = reverse_lazy('customers:union-list')
    success_message = 'A new union is successfully created.'
    page_name = 'unions'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'customer_list': Customer.objects.all(),
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response
