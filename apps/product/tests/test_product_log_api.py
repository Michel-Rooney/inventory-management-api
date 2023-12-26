from django.urls import reverse
from rest_framework import status

from .base_product import BaseProductApiTest


class ProductApiTest(BaseProductApiTest):
    def test_product_product_log_api_list_return_status_code_200_success(self):
        url = reverse("product:log-product-api-list")
        token = self.get_jwt_token()

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
