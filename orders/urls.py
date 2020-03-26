from django.urls import path

from .views import OpenOrderListView, OrderCreateView


app_name = 'orders'


urlpatterns = [
    path('', OpenOrderListView.as_view(), name='open-orders-list'),
    path('create', OrderCreateView.as_view(), name='order-create')
]
