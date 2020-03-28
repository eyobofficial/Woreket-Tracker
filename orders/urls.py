from django.urls import path

from .views import OpenOrderListView, OrderCreateView, OrderUpdateView, \
    OrderCloseView, OrderDetailView, AllocationCreateView, \
    AllocationUpdateView, AllocationDeleteView


app_name = 'orders'


urlpatterns = [
    path('', OpenOrderListView.as_view(), name='open-orders-list'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='open-order-detail'),
    path('create/', OrderCreateView.as_view(), name='open-order-create'),
    path(
        '<uuid:pk>/update/',
        OrderUpdateView.as_view(),
        name='open-order-update'
    ),
    path(
        '<uuid:pk>/close/',
        OrderCloseView.as_view(),
        name='order-close'
    ),
    path(
        '<uuid:pk>/allocations/create/',
        AllocationCreateView.as_view(),
        name='order-allocation-create'
    ),
    path(
        'allocations/<uuid:pk>/update/',
        AllocationUpdateView.as_view(),
        name='open-allocation-update'
    ),
    path(
        'allocations/<uuid:pk>/delete/',
        AllocationDeleteView.as_view(),
        name='allocation-delete'
    )
]
