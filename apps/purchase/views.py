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

        for product in products:
            instance = querys.get_product(name=product.get("name"))

            log_product_exits = querys.get_products_expiration_log(
                product=instance
            ).exists()

            if log_product_exits:
                quantity = instance.quantity - product.get("quantity", "")
                expiration = product.get("expiration", instance.expiration)
                analyze_expiration(instance, quantity, expiration)

        return super().perform_create(serializer)

    @action(["get"], False)
    def dashboard_data(self, request, *args, **kwargs):
        types = ["week", "month", "year"]
        request_type = request.query_params.get("type", "")

        if request_type not in types:
            return Response({"detail": "Tipo de atributo da url inválido."})

        if request_type == "week":
            data = dashboard_data.get_date_values(6, "%A", "days")

        elif request_type == "month":
            data = dashboard_data.get_date_values(30, "%d/%b", "days")

        elif request_type == "year":
            data = dashboard_data.get_date_values(11, "%B", "months")

        return Response(data)
