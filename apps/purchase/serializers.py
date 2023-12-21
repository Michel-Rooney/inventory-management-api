from rest_framework import serializers
from . import models


class PurchaseSerializer(serializers.ModelSerializer):
    products = serializers.ListField(required=True)

    class Meta:
        model = models.Purchase
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('products')
        return super().create(validated_data)


