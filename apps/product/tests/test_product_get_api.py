from django.urls import reverse
from rest_framework import status

from .base_product import BaseProductApiTest


class ProductApiTest(BaseProductApiTest):
    """
                                    Product
    """

    def test_product_product_api_list_return_status_code_200_success(self):
        QUANTITY = 3
        admin_data = {"username": "admin", "password": "adminpass"}
        admin = self.create_super_user(**admin_data)
        self.create_amost_product(QUANTITY, admin)

        url = reverse("product:product-api-list")
        token = self.get_jwt_token(**admin_data, create_user=False)

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        count_response = response.data.get("count")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(QUANTITY, count_response)

    def test_product_product_api_list_return_empty_products(self):
        admin_data = {"username": "AnotherAdmin", "password": "adminpass"}
        admin = self.create_super_user(**admin_data)
        self.create_amost_product(3, admin)

        url = reverse("product:product-api-list")
        token = self.get_jwt_token()

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        count_response = response.data.get("count")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, count_response)

    def test_produt_product_api_detail_return_status_code_200_success(self):
        admin_data = {"username": "admin", "password": "adminpass"}
        admin = self.create_super_user(**admin_data)
        product = self.create_product(company=admin)

        url = reverse("product:product-api-detail", args=(product.id,))
        token = self.get_jwt_token(**admin_data, create_user=False)

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_produt_product_api_detail_return_status_code_403_forbidden(self):
        admin_data = {"username": "AnotherAdmin", "password": "adminpass"}
        admin = self.create_super_user(**admin_data)
        product = self.create_product(company=admin)

        url = reverse("product:product-api-detail", args=(product.id,))
        token = self.get_jwt_token()

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_produt_product_api_search_return_correct_search(self):
        PRODUCT_NAME = 'Product 1'
        admin_data = {"username": "AnotherAdmin", "password": "adminpass"}
        admin = self.create_super_user(**admin_data)
        self.create_amost_product(3, admin)

        url = reverse("product:product-api-list") + f'?search={PRODUCT_NAME}'
        token = self.get_jwt_token(**admin_data, create_user=False)

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        entity = response.data.get('results')[0]

        self.assertEqual(PRODUCT_NAME, entity.get('name'))
        self.assertEqual(1, response.data.get('count'))

    def test_produt_product_api_search_return_empty_products(self):
        PRODUCT_NAME = 'Product 1'
        admin_data = {"username": "AnotherAdmin", "password": "adminpass"}
        admin = self.create_super_user(**admin_data)
        self.create_amost_product(3, admin)

        url = reverse("product:product-api-list") + f'?search={PRODUCT_NAME}'
        token = self.get_jwt_token()

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        count = response.data.get('count')

        self.assertEqual(0, count)
