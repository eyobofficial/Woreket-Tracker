from django.urls import path

from .views.batches import OpenBatchListView, BatchCreateView, BatchUpdateView, \
    BatchDeleteView, BatchDetailView, SupplierPopupView
from .views.deliveryorders import OpenOrderListView, OrderCreateView, \
    OrderUpdateView, OrderDetailView, OrderDeleteView
from .views.allocations import AllocationCreateView, AllocationUpdateView, \
    AllocationDeleteView, LetterFormView, AllocationLetterView, \
    AllocationDetailView
from .views.distributions import DistributionCreateView, \
    DistributionUpdateView, DistributionDeleteView, DistributionDetailView


app_name = 'orders'

urlpatterns = [
    path('', OpenOrderListView.as_view(), name='open-orders-list'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path(
        '<uuid:batch_pk>/create/',
        OrderCreateView.as_view(),
        name='order-create'
    ),
    path(
        '<uuid:pk>/update/',
        OrderUpdateView.as_view(),
        name='order-update'
    ),
    path(
        '<uuid:pk>/delete/',
        OrderDeleteView.as_view(),
        name='order-delete'
    ),
    path(
        '<uuid:pk>/letter-form/',
        LetterFormView.as_view(),
        name='order-letter-form'
    ),
    path(
        '<uuid:pk>/allocation-letter/',
        AllocationLetterView.as_view(),
        name='order-allocation-letter'
    ),
    path(
        'allocations/<uuid:pk>/',
        AllocationDetailView.as_view(),
        name='order-allocation-detail'
    ),
    path(
        '<uuid:pk>/allocations/create/',
        AllocationCreateView.as_view(),
        name='order-allocation-create'
    ),
    path(
        'allocations/<uuid:pk>/update/',
        AllocationUpdateView.as_view(),
        name='order-allocation-update'
    ),
    path(
        'allocations/<uuid:pk>/delete/',
        AllocationDeleteView.as_view(),
        name='allocation-delete'
    ),
    path(
        'distributions/<uuid:pk>/',
        DistributionDetailView.as_view(),
        name='order-distribution-detail'
    ),
    path(
        '<uuid:pk>/distributions/create/',
        DistributionCreateView.as_view(),
        name='order-distribution-create'
    ),
    path(
        'distributions/<uuid:pk>/update/',
        DistributionUpdateView.as_view(),
        name='order-distribution-update'
    ),
    path(
        'distribution/<uuid:pk>/delete/',
        DistributionDeleteView.as_view(),
        name='distribution-delete'
    ),
]


# Batch URLs
urlpatterns += [
    path('batches/', OpenBatchListView.as_view(), name='open-batch-list'),
    # path(
    #     'batches/closed/',
    #     ClosedBatchListView.as_view(),
    #     name='closed-batch-list'
    # ),
    path('batches/create/', BatchCreateView.as_view(), name='batch-create'),
    path('batches/<uuid:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path(
        'batches/<uuid:pk>/update/',
        BatchUpdateView.as_view(),
        name='batch-update'
    ),
    path(
        'batches/<uuid:pk>/delete/',
        BatchDeleteView.as_view(),
        name='batch-delete'
    ),
   path(
        'supplier/<uuid:pk>/popup/',
        SupplierPopupView.as_view(),
        name='supplier-popup'
    ),
]
