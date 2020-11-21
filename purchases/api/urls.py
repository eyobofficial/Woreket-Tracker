from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .viewsets import SupplierViewSet, ProductViewSet


app_name = 'purchases'

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = router.urls
