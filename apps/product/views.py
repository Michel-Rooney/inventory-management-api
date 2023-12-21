from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.decorators import action

from apps.utils import querys

from . import serializers, models
from apps.permissions import IsOwnerProduct
from apps.utils.product.product import get_products_alert
from apps.utils.product.expiration import analyze_expiration
from .pagination import ProductPagination


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
        instance = serializer.instance
        quantity = self.request.data.get('quantity', '')
        expiration = self.request.data.get(
            'expiration', str(instance.expiration)
        )

        analyze_expiration(instance, quantity, expiration)
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
