from rest_framework import serializers

from purchases.models import Supplier, Product


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    unit = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'
