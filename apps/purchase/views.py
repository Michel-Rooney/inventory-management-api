from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.permissions import IsOwnerProduct
from apps.purchase import serializers
from apps.utils import querys
from apps.utils.product.expiration import analyze_expiration
from apps.utils.purchase import (dashboard_data, validators,
                                 validators_request_data)


class PurchaseViewSets(ModelViewSet):
    queryset = querys.get_purchases()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [IsAuthenticated, IsOwnerProduct]
    http_method_names = ["get", "post", "PUT", "PATCH", "DELETE"]

    def list(self, request, *args, **kwargs):
        return Response({
            "detail": 'Método "GET" não é permitido.'
        }, status=405)

    def retrieve(self, request, *args, **kwargs):
        return Response({
            "detail": 'Método "GET" não é permitido.'
        }, status=405)

    def perform_create(self, serializer):
        products = self.request.data["products"]

        validators_request_data.analyze_request_data(products)
        validators.analyze_product_model_existence(products)

        company = self.request.user
        validators.analyze_product_save(serializer, company, products)

        total_price = 0
        total_purchase_price = 0

        for product in products:
            total_price += (
                product.get('quantity') * product.get('sale_price')
            )
            total_purchase_price += (
                product.get('quantity') * product.get('purchase_price')
            )

            instance = querys.get_product(name=product.get("name"))

            log_product_exits = querys.get_products_expiration_log(
                product=instance
            ).exists()

            if log_product_exits:
                quantity = instance.quantity - product.get("quantity", "")
                expiration = product.get("expiration", instance.expiration)
                analyze_expiration(instance, quantity, expiration)

        serializer.validated_data['total_price'] = total_price
        serializer.validated_data[
            'total_purchase_price'
        ] = total_purchase_price
        return super().perform_create(serializer)

    @action(["get"], False)
    def dashboard_data(self, request, *args, **kwargs):
        types = ["week", "month", "year"]
        request_type = request.query_params.get("type", "")

        if request_type not in types:
            return Response({"detail": "Tipo de atributo da url inválido."})

        company = request.user.id

        if request_type == "week":
            data = dashboard_data.get_date_values(company, 6, "%A", "days")

        elif request_type == "month":
            data = dashboard_data.get_date_values(company, 30, "%d/%b", "days")

        elif request_type == "year":
            data = dashboard_data.get_date_values(
                company, 11, "%B", "months", is_year=True
            )

        return Response(data)
