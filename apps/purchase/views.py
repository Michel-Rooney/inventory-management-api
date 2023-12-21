from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.utils.product.expiration import analyze_expiration
from apps.utils.purchase import validators, validators_request_data
from apps.permissions import IsOwnerProduct

from apps.utils import querys
from apps.purchase import serializers


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

        for product in products:
            instance = querys.get_product(
                name=product.get('name')
            )
            quantity = instance.quantity - product.get('quantity', '')
            expiration = product.get(
                'expiration', instance.expiration
            )
            analyze_expiration(instance, quantity, expiration)

        return super().perform_create(serializer)
