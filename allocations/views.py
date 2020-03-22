from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from shared.models import Region, Location, Union

from .mixins import BaseAllocationView
from .models import DistributionOrder, Allocation, LC, Fertilizer


class DistributionListView(BaseAllocationView, ListView):
    """
    Distribution order list view.
    """
    template_name = 'allocations/distribution_list.html'
    model = DistributionOrder
    ordering = '-created_at'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_deleted=False)


class DistributionCreateView(BaseAllocationView, CreateView):
    """
    Creates new distribution order.
    """
    template_name = 'allocations/modals/distribution_create.html'
    model = DistributionOrder
    fields = ('lc', 'vessel', 'fertilizer')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'lc_list': LC.objects.all(),
            'fertilizers': Fertilizer.objects.all()
        })
        return super().get_context_data(**kwargs)


class DistributionDetailView(BaseAllocationView, DetailView):
    """
    Distribution order detail view.
    """
    template_name = 'allocations/distribution_detail.html'
    model = DistributionOrder


class AllocationCreateView(BaseAllocationView, CreateView):
    """
    Allocation create view.
    """
    template_name = 'allocations/modals/allocation_create.html'
    model = Allocation
    fields = ('region', 'location', 'union', 'quantity')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'regions': Region.objects.all(),
            'locations': Location.objects.all(),
            'unions': Union.objects.all()
        })
        return super().get_context_data(**kwargs)

    def get_distribution_order(self):
        pass

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        distribution_order = DistributionOrder.objects.get(pk=pk)
        allocation = form.save(commit=False)
        allocation.distribution_order = distribution_order
        allocation.created_by = self.request.user
        return redirect('allocations:allocation-detail', args=[allocation.pk])

    def form_invalid(self, form):
        print('\n\n', form.errors, end='\n\n')
        return super().form_invalid(form)
