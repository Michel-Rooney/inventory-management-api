from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .base_product import BaseProductApiTest


class ProductApiTest(BaseProductApiTest):
    """
                                    Product
    """

    def test_product_product_api_alert_return_status_code_200_success(self):
        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token()
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_product_product_api_alert_return_red_expiration_data(self):
        EXPIRATION = (timezone.now() + timezone.timedelta(days=2)).date()
        admin_data = {'username': 'Admin', 'password': 'Password'}
        admin = self.create_super_user(**admin_data)

        self.create_product(
            company=admin,
            name='Product 01',
            expiration=EXPIRATION
        )

        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        count = len(response.data)
        entity = response.data[0]

        self.assertEqual(1, count)
        self.assertEqual(str(EXPIRATION), entity.get('expiration'))
        self.assertEqual('date_red', entity.get('status'))

    def test_product_product_api_alert_return_yellow_expiration_data(self):
        EXPIRATION = (timezone.now() + timezone.timedelta(days=3)).date()
        admin_data = {'username': 'Admin', 'password': 'Password'}
        admin = self.create_super_user(**admin_data)

        self.create_product(
            company=admin,
            name='Product 01',
            expiration=EXPIRATION
        )

        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        count = len(response.data)
        entity = response.data[0]

        self.assertEqual(1, count)
        self.assertEqual(str(EXPIRATION), entity.get('expiration'))
        self.assertEqual('date_yellow', entity.get('status'))

    def test_product_product_api_alert_return_empty_expiration_data(self):
        admin_data = {'username': 'Admin', 'password': 'Password'}
        admin = self.create_super_user(**admin_data)

        self.create_product(
            company=admin,
            name='Product 01',
            expiration='2023-12-20'
        )

        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token()
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(0, len(response.data))

    def test_product_product_api_alert_return_red_quantity_product(self):
        QUANTITY = 2
        admin_data = {'username': 'Admin', 'password': 'Password'}
        admin = self.create_super_user(**admin_data)

        self.create_product(
            company=admin,
            name='Product 01',
            quantity=QUANTITY
        )

        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        count = len(response.data)
        entity = response.data[0]

        self.assertEqual(1, count)
        self.assertEqual(QUANTITY, entity.get('quantity'))
        self.assertEqual('quantity_red', entity.get('status'))

    def test_product_product_api_alert_return_yellow_quantity_product(self):
        QUANTITY = 3
        admin_data = {'username': 'Admin', 'password': 'Password'}
        admin = self.create_super_user(**admin_data)

        self.create_product(
            company=admin,
            name='Product 01',
            quantity=QUANTITY
        )

        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        count = len(response.data)
        entity = response.data[0]

        self.assertEqual(1, count)
        self.assertEqual(QUANTITY, entity.get('quantity'))
        self.assertEqual('quantity_yellow', entity.get('status'))

    def test_product_product_api_alert_return_empty_quantity_product(self):
        admin_data = {'username': 'Admin', 'password': 'Password'}
        admin = self.create_super_user(**admin_data)

        self.create_product(
            company=admin,
            name='Product 01',
            quantity=0,
        )

        url = reverse('product:product-api-alert-products')
        token = self.get_jwt_token()
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(0, len(response.data))
