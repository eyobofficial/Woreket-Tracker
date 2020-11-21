from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .viewsets import PortViewSet


app_name = 'orders-api'

router = DefaultRouter()
router.register('ports', PortViewSet)

urlpatterns = [
    path('', include(router.urls))
]
