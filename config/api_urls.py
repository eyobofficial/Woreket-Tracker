from django.urls import path, include

from rest_framework import routers


app_name = 'api'

urlpatterns = [
    path('', include('orders.api.urls')),
    path('', include('purchases.api.urls')),
]
