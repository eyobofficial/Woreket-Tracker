from django.urls import path

from .views import DeliveryOrderOverview, DeliveryOrderCreateView


app_name = 'orders'


urlpatterns = [
    path('', DeliveryOrderOverview.as_view(), name='overview'),
    path(
        'create',
        DeliveryOrderCreateView.as_view(),
        name='delivery-order-create'
    )
]
