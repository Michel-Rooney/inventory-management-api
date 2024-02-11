from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.utils.permissions import IsOwnerProduct
from apps.purchase import serializers
from apps.utils import querys
from apps.utils.purchase import dashboard_data, purchase


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
        purchase.create_purchase(self, serializer)
        return super().perform_create(serializer)

    @action(["get"], False)
    def dashboard_data(self, request, *args, **kwargs):
        data = dashboard_data.get_dashboard_data(request)
        return Response(data, content_type='application/json')
