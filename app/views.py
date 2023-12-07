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
        # 1- Preciso pegar os dados da request
        instance = serializer.instance
        quantity = self.request.data.get('quantity', '')
        expiration = self.request.data.get(
            'expiration', str(instance.expiration)
        )

        if quantity == '':
            return super().perform_update(serializer)

        diff_quantity = quantity - instance.quantity
        
        # 2- Preciso pegar o antigo_model do ValidatyProduct apartir do id e da data
        before_model = models.ProductExpirationLog.objects.filter(
            product__id=instance.id,
            expiration=instance.expiration
        ).first()

        # 3- Validar se o antigo_model realmente existe
        #     1. Se existir, passa a diante
        #     2. Se não existir, criar novo model apartir da diferença
        if not before_model:
            models.ProductExpirationLog.objects.create(
                product=instance,
                quantity=diff_quantity,
                expiration=instance.expiration
            )
            return super().perform_update(serializer)
        
        print(diff_quantity)
        

        # 4- Preciso validar se datas são iguais/diferentes
        #     1. Se iguais, preciso analisar se a diferença é positiva ou negativa
        if expiration != str(before_model.expiration):
        #     1. Se a diferença é positiva, criar novo model
            if diff_quantity > 0:
                actual_model = models.ProductExpirationLog.objects.filter(
                    product__id=instance.id,
                    expiration=expiration
                ).first()

                models.ProductExpirationLog.objects.create(
                    product=instance,
                    quantity=diff_quantity,
                    expiration=expiration
                )

        #     2. Se a diferença é negativa, tirar do antigo_model
            else:
                before_model.quantity += diff_quantity
                before_model.save()

        #         1. Se o antigo_model ficar menor que 0, então deleta-lo
                if before_model.quantity == 0:
                    before_model.delete()
                
                if before_model.quantity < 0:
                    actual_model = models.ProductExpirationLog.objects.filter(
                        product__id=instance.id,
                        expiration=expiration
                    ).first()

                    actual_model += diff_quantity
                    actual_model.save()
                    
                    before_model.delete()

        #     2. Se diferentes, preciso analisar se a diferença é positva ou negativa
        else:
            #     1. Se a diferença é positiva, adicionar ao antigo_model
            if diff_quantity >= 0:
                before_model.quantity += diff_quantity
                before_model.save()

        #     2. Se a diferença negativa, tirar do antigo_model já existente
            else:

                before_model = models.ProductExpirationLog.objects.filter(
                    product__id=instance.id
                ).first()

                before_model.quantity += diff_quantity
                before_model.save()

        #         1. Se o antigo_model ficar menor que 0, então deleta-lo
                if before_model.quantity == 0:
                    before_model.delete()

                if before_model.quantity < 0:
                    actual_model = models.ProductExpirationLog.objects.filter(
                        product__id=instance.id,
                        expiration=expiration
                    ).first()

                    actual_model += diff_quantity
                    actual_model.save()

                    before_model.delete()
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
