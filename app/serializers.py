from django.contrib.auth.models import User
from rest_framework import serializers
from . import models
from collections import defaultdict
from rest_framework.validators import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name'
        ]


class ProductSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = defaultdict(list)

    class Meta:
        model = models.Product
        fields = '__all__'

    def validade(self, attrs):
        if self.messages:
            raise ValidationError(self.messages)

        return super().validate(attrs)
