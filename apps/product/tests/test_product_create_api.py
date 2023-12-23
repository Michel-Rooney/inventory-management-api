from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .base_product import BaseProductApiTest


class ProductCreateApiTest(BaseProductApiTest):
    def test_product_product_api_create_return_status_code_201_created(self):
        EXPIRATION = timezone.now().date()
        admin_data = {'username': 'Admin', 'password': 'Pass'}
        admin = self.create_super_user(**admin_data)

        data = {
            'company': admin,
            'name': 'Product',
            'description': 'Description',
            'brand': 'Brand',
            'quantity': 10,
            'purchase_price': 10,
            'sale_price': 11,
            'expiration': EXPIRATION,
        }

        url = reverse('product:product-api-list')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
