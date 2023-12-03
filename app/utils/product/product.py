from app import serializers
from app.utils import querys


def get_products_alert(request):
    products_yellow = querys.get_products(
        quantity__range=[3, 5], company=request.user
    )
    products_red = querys.get_products(
        quantity__range=[0, 2], company=request.user
    )

    serializer_yellow = serializers.ProductSerializer(
        products_yellow, many=True
    ).data
    for product in serializer_yellow:
        product['status'] = 'yellow'

    serializer_red = serializers.ProductSerializer(
        products_red, many=True
    ).data
    for product in serializer_red:
        product['status'] = 'red'

    result_products = serializer_red + serializer_yellow
    return result_products
