from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.utils.permissions import IsOwnerProduct
from apps.utils import querys
from apps.utils.product import expiration as product_expiration
from apps.utils.product.alert import get_products_alert

from . import serializers
from .pagination import ProductPagination


class ProductViewSets(ModelViewSet):
    queryset = querys.get_products()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerProduct]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'brand']
    pagination_class = ProductPagination

    def perform_create(self, serializer):
        product_expiration.create_expiration(self, serializer)
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        product_expiration.update_expiration(self, serializer)
        return super().perform_update(serializer)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(company=request.user.id)
        return super().list(request, *args, **kwargs)

    @action(['get'], False)
    def alert_products(self, request, *args, **kwargs):
        result_products = get_products_alert(request)
        return Response(result_products)


class ProductLogViewSets(ModelViewSet):
    queryset = querys.get_log_products()
    serializer_class = serializers.ProductLogSerializer
