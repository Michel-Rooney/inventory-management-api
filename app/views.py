from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.decorators import action

from .utils import querys

from . import serializers, models
from .permissions import IsOwner, IsOwnerProduct
from .utils.purchase import validators, validators_request_data
from .utils.product.product import get_products_alert
from .utils.product.expiration import analyze_expiration
from .pagination import ProductPagination


class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'POST', 'PUT', 'PATCH', 'DELETE']
    permission_classes = [IsOwner, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        obj = get_object_or_404(User, id=request.user.id)
        serializers = self.get_serializer(
            instance=obj
        )
        return Response(serializers.data)


class ProductViewSets(ModelViewSet):
    queryset = querys.get_products()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerProduct]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'brand']
    pagination_class = ProductPagination

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

        expiration_log = models.ProductExpirationLog.objects.create(
            product=serializer.instance,
            quantity=serializer.instance.quantity,
            expiration=serializer.instance.expiration
        )

        expiration_log.save()

        return super().perform_create(serializer)

    def perform_update(self, serializer):
        analyze_expiration(self, serializer)
        return super().perform_update(serializer)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(company=request.user.id)
        return super().list(request, *args, **kwargs)

    @action(['get'], False)
    def alert_products(self, request, *args, **kwargs):
        result_products = get_products_alert(request)
        return Response(result_products)


class PurchaseViewSets(ModelViewSet):
    queryset = querys.get_purchases()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [IsAuthenticated, IsOwnerProduct]
    http_method_names = ['get', 'post', 'PUT', 'PATCH', 'DELETE']

    def perform_create(self, serializer):
        products = self.request.data['products']

        validators_request_data.analyze_request_data(products)
        validators.analyze_product_model_existence(products)

        company = self.request.user
        validators.analyze_product_save(serializer, company, products)

        return super().perform_create(serializer)


class ProductLogViewSets(ModelViewSet):
    queryset = querys.get_log_products()
    serializer_class = serializers.ProductLogSerializer
