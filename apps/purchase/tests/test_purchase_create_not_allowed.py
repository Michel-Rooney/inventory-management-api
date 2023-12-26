from django.urls import reverse
from rest_framework import status

from .base_purchase import BasePurchaseApiTest


class PurchaseCreateNotAllowedApiTest(BasePurchaseApiTest):
    def test_purchase_api_post_return_status_code_http_401_unauthorized(self):
        url = reverse('purchase:purchase-api-list')
        response = self.client.post(url)

        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        )

    def test_purchase_api_list_return_status_code_405_method_not_allowed(self):
        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(
            status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code
        )

    def test_purchase_api_retrieve_return_405_method_not_allowed(self):
        url = reverse('purchase:purchase-api-detail', args=(1,))
        token = self.get_jwt_token()
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(
            status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code
        )

    def test_purchase_api_put_return_status_code_405_method_not_allowed(self):
        url = reverse('purchase:purchase-api-detail', args=(1,))
        token = self.get_jwt_token()
        response = self.client.put(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(
            status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code
        )

    def test_purchase_api_delete_return_405_method_not_allowed(self):
        url = reverse('purchase:purchase-api-detail', args=(1,))
        token = self.get_jwt_token()
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(
            status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code
        )
