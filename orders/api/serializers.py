from shared.api.serializers import UUIDModelSerializer

from orders.models import Port


class PortSerializer(UUIDModelSerializer):

    class Meta:
        model = Port
        fields = ('id', 'name', 'country', 'office', 'is_default')
