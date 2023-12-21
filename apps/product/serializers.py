from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            'id', 'name', 'description', 'brand',
            'quantity', 'purchase_price', 'sale_price',
            'expiration'
        ]


class ProductLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductLog
        fields = '__all__'
