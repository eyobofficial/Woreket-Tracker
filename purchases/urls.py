from django.urls import path

from .views import ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, SupplierListView, SupplierCreateView, \
    SupplierUpdateView, SupplierDeleteView


app_name = 'purchases'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path(
        'products/create/',
        ProductCreateView.as_view(),
        name='product-create'
    ),
    path(
        'products/<uuid:pk>/update/',
        ProductUpdateView.as_view(),
        name='product-update'
    ),
    path(
        'products/<uuid:pk>/delete/',
        ProductDeleteView.as_view(),
        name='product-delete'
    ),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path(
        'suppliers/create/',
        SupplierCreateView.as_view(),
        name='supplier-create'
    ),
    path(
        'suppliers/<uuid:pk>/update/',
        SupplierUpdateView.as_view(),
        name='supplier-update'
    ),
    path(
        'suppliers/<uuid:pk>/delete/',
        SupplierDeleteView.as_view(),
        name='supplier-delete'
    ),
]
