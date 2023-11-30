from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name'
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    products = serializers.ListField(required=True)

    class Meta:
        model = models.Purchase
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('products')
        return super().create(validated_data)


class LogProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogProduct
        fields = '__all__'
