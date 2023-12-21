from django.utils import timezone
from apps.product import serializers
from apps.utils import querys


QUANTITY_RED = 'quantity_red'
QUANTITY_YELLOW = 'quantity_yellow'

DATE_RED = 'date_red'
DATE_YELLOW = 'date_yellow'


def get_serializer_data_product(product, status):
    serializer_data = serializers.ProductSerializer(
        product, many=True
    ).data

    for item in serializer_data:
        item['status'] = status

    return serializer_data


def get_products_alert_quantity(request):
    products_yellow = querys.get_products(
        quantity__range=[3, 5], company=request.user
    ).order_by('quantity')
    products_red = querys.get_products(
        quantity__range=[0, 2], company=request.user
    ).order_by('quantity')

    serializer_yellow = get_serializer_data_product(products_yellow, QUANTITY_YELLOW)
    serializer_red = get_serializer_data_product(products_red, QUANTITY_RED)

    result_products = serializer_red + serializer_yellow
    return result_products


def get_products_alert_expiration_date(request):
    minimal_date = (timezone.now() + timezone.timedelta(days=3)).date()    
    future_date = (timezone.now() + timezone.timedelta(days=10)).date()

    products_yellow = querys.get_products(
        expiration__range=[minimal_date, future_date],
        company=request.user
    ).order_by('expiration')
    
    products_red = querys.get_products(
        expiration__lt=minimal_date,
        company=request.user 
    ).order_by('expiration')

    serializer_yellow = get_serializer_data_product(products_yellow, DATE_YELLOW)
    serializer_red = get_serializer_data_product(products_red, DATE_RED)

    result_products = serializer_red + serializer_yellow
    return result_products

def get_products_alert(request):
    alert_quantity = get_products_alert_quantity(request)
    alert_expiration_date = get_products_alert_expiration_date(request)

    result_products = alert_quantity + alert_expiration_date
    return result_products
