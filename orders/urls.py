from django.urls import path

from .views import OpenOrderListView, OrderCreateView, OrderUpdateView, \
    OrderCloseView, OrderDetailView, AllocationCreateView, \
    AllocationUpdateView, AllocationDeleteView, LetterFormView, \
    AllocationLetterView, DistributionCreateView, DistributionUpdateView, \
    DistributionDeleteView, DistributionDetailView, ClosedOrderListView, \
    OrderReopenView, OrderDeleteView


app_name = 'orders'


urlpatterns = [
    path('', OpenOrderListView.as_view(), name='open-orders-list'),
    path('closed/', ClosedOrderListView.as_view(), name='closed-orders-list'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path(
        '<uuid:pk>/update/',
        OrderUpdateView.as_view(),
        name='open-order-update'
    ),
    path(
        '<uuid:pk>/delete/',
        OrderDeleteView.as_view(),
        name='order-delete'
    ),
    path(
        '<uuid:pk>/open/',
        OrderReopenView.as_view(),
        name='order-open'
    ),
    path(
        '<uuid:pk>/close/',
        OrderCloseView.as_view(),
        name='order-close'
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
