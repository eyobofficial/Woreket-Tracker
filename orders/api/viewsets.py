from rest_framework.viewsets import ReadOnlyModelViewSet

from orders.models import Port
from .serializers import PortSerializer


class PortViewSet(ReadOnlyModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer
    lookup_field = 'uuid'
