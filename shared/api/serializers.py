from rest_framework import serializers


class UUIDModelSerializer(serializers.ModelSerializer):
    """
    Base model serializer class that uses the `uuid` field
    as the `id` field.
    """
    id = serializers.ReadOnlyField(source='uuid')
