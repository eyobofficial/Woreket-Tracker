from django.urls import path

from .views.batches import OpenBatchListView, ClosedBatchListView, \
    BatchCreateView, BatchUpdateView, BatchCloseView, BatchReopenView, \
    BatchDeleteView, BatchDetailView, SupplierPopupView
from .views.deliveryorders import OrderCreateView, \
    OrderUpdateView, OrderDetailView, OrderDeleteView
from .views.allocations import AllocationCreateView, AllocationUpdateView, \
    AllocationDeleteView, LetterFormView, AllocationLetterView, \
    AllocationDetailView
from .views.distributions import DistributionCreateView, \
    DistributionUpdateView, DistributionDeleteView, DistributionDetailView


app_name = 'orders'

urlpatterns = [
    path('', OpenBatchListView.as_view(), name='open-batch-list'),
    path(
        'batches/closed/',
        ClosedBatchListView.as_view(),
        name='closed-batch-list'
    ),
    path('batches/create/', BatchCreateView.as_view(), name='batch-create'),
    path('batches/<uuid:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path(
        'batches/<uuid:pk>/update/',
        BatchUpdateView.as_view(),
        name='batch-update'
    ),
    path(
        'batches/<uuid:pk>/close/',
        BatchCloseView.as_view(),
        name='batch-close'
    ),
    path(
        'batches/<uuid:pk>/reopen/',
        BatchReopenView.as_view(),
        name='batch-reopen'
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
    path(
        'delivery-orders/<uuid:pk>/',
        OrderDetailView.as_view(),
        name='order-detail'
    ),
    path(
        '<uuid:batch_pk>/delivery-orders/create/',
        OrderCreateView.as_view(),
        name='order-create'
    ),
    path(
        'delivery-orders/<uuid:pk>/update/',
        OrderUpdateView.as_view(),
        name='order-update'
    ),
    path(
        'delivery-orders/<uuid:pk>/delete/',
        OrderDeleteView.as_view(),
        name='order-delete'
    ),
    path(
        'delivery-orders/<uuid:pk>/letter-form/',
        LetterFormView.as_view(),
        name='order-letter-form'
    ),
    path(
        'delivery-orders/<uuid:pk>/allocation-letter/',
        AllocationLetterView.as_view(),
        name='order-allocation-letter'
    ),
    path(
        'allocations/<uuid:pk>/',
        AllocationDetailView.as_view(),
        name='order-allocation-detail'
    ),
    path(
        'delivery-orders/<uuid:pk>/allocations/create/',
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
        'delivery-orders/<uuid:pk>/distributions/create/',
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
