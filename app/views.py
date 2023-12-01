from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from . import models, serializers
from .permissions import IsOwner, IsOwnerProduct
from .utils.purchase import analyze_product_save


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
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerProduct]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'brand']

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(company=request.user.id)
        return super().list(request, *args, **kwargs)


class PurchaseViewSets(ModelViewSet):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [IsAuthenticated, IsOwnerProduct]
    http_method_names = ['get', 'post', 'PUT', 'PATCH', 'DELETE']

    def perform_create(self, serializer):
        purchase_instance = serializer.save(company=self.request.user)

        products = self.request.data['products']
        analyze_product_save(purchase_instance, products)

        return super().perform_create(serializer)


class LogProductViewSets(ModelViewSet):
    queryset = models.LogProduct.objects.all()
    serializer_class = serializers.LogProductSerializer
