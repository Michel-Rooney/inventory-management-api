from . import models, serializers
from rest_framework.viewsets import ModelViewSet


class ProductViewSets(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
