from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF
from shared.models import Unit

from .forms import BatchForm
from .mixins import BasePurchasesView
from .models import Batch, ProductCategory, Product, Supplier


class BatchListView(BasePurchasesView, ListView):
    """List view of purchasing batches (lots)."""
    template_name = 'purchases/batch_list.html'
    model = Batch
    paginate_by = 10
    page_name = 'batches'
    queryset = Batch.objects.all()
    access_roles = [ROLE_STAFF, ROLE_MANAGEMENT, ROLE_ADMIN]

    def get_queryset(self):
        qs = super().get_queryset()
        product_pk = self.request.GET.get('product')
        search_query = self.request.GET.get('search')

        if product_pk is not None:
            qs = qs.filter(product__pk=product_pk)

        if search_query is not None:
            qs = self.get_search_result(search_query)

        return qs

    def get_context_data(self, **kwargs):
        kwargs['product_list'] = Product.objects.all()
        kwargs['selected_product'] = self.request.GET.get('product')
        kwargs['batch_count'] = self.queryset.count()
        kwargs['search_query'] = self.request.GET.get('search', '').strip()
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns a batches using search query."""
        search_qs = self.queryset.filter(
            Q(name__icontains=query) |
            Q(year__icontains=query) |
            Q(product__name__icontains=query) |
            Q(supplier__name__icontains=query)
        )
        return search_qs


class BatchDetailView(BasePurchasesView, DetailView):
    """Detail view for a purchasing batch instance."""
    template_name = 'purchases/modals/batches/batch_detail.html'
    model = Batch
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(is_deleted=True)
        return qs


class BatchCreateView(BasePurchasesView, SuccessMessageMixin, CreateView):
    """Create view for creating purchasing batch."""
    template_name = 'purchases/modals/batches/batch_form.html'
    form_class = BatchForm
    model = Batch
    success_url = reverse_lazy('purchases:batch-list')
    success_message = 'A new LOT record is successfully created.'
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'supplier_list': Supplier.objects.all(),
            'product_list': Product.objects.all(),
            'year_choice_list': Batch.YEAR_CHOICES
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class BatchUpdateView(BasePurchasesView, SuccessMessageMixin, UpdateView):
    """Update view for editing purchasing batch."""
    template_name = 'purchases/modals/batches/batch_form.html'
    form_class = BatchForm
    model = Batch
    success_url = reverse_lazy('purchases:batch-list')
    success_message = 'The LOT data is successfully updated.'
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'supplier_list': Supplier.objects.all(),
            'product_list': Product.objects.all(),
            'year_choice_list': Batch.YEAR_CHOICES
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class BatchDeleteView(BasePurchasesView, SuccessMessageMixin, DeleteView):
    """Delete view to delete purchasing batch."""
    template_name = 'purchases/modals/batches/batch_delete_form.html'
    model = Batch
    success_url = reverse_lazy('purchases:batch-list')
    success_message = 'The selected LOT is successfully deleted.'
    page_name = 'batches'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def delete(self, request, *args, **kwargs):
        """Overwrites delete method to change is_delete status `True`."""
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        success_url = self.get_success_url()
        messages.success(request, self.success_message)
        return redirect(success_url)


class ProductListView(BasePurchasesView, ListView):
    """List view of fertilier products."""
    template_name = 'purchases/product_list.html'
    model = Product
    paginate_by = 10
    page_name = 'products'
    queryset = Product.objects.all()
    access_roles = [ROLE_STAFF, ROLE_MANAGEMENT, ROLE_ADMIN]

    def get_queryset(self):
        qs = super().get_queryset()
        category_pk = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        if category_pk is not None:
            qs = qs.filter(category__pk=category_pk)

        if search_query is not None:
            qs = self.get_search_result(search_query)

        return qs

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = ProductCategory.objects.all()
        kwargs['selected_category'] = self.request.GET.get('category')
        kwargs['product_count'] = self.queryset.count()
        kwargs['search_query'] = self.request.GET.get('search', '').strip()
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns a batches using search query."""
        search_qs = self.queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        return search_qs


class ProductCreateView(BasePurchasesView, SuccessMessageMixin, CreateView):
    """Create view for creating product."""
    template_name = 'purchases/modals/products/product_form.html'
    model = Product
    fields = ('name', 'category', 'unit')
    success_url = reverse_lazy('purchases:product-list')
    success_message = 'A new product is successfully created.'
    page_name = 'products'
    access_roles = [ROLE_ADMIN, ROLE_STAFF]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'category_list': ProductCategory.objects.all(),
            'unit_list': Unit.objects.all()
        })
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response
