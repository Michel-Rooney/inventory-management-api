from django.test import TestCase
from django.urls import reverse
from rest_framework import status, test


class ProductJWTApiTest(test.APITestCase, TestCase):
    def test_product_jwt_product_list_return_401_unauthorized(self):
        url = reverse("product:product-api-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_detail_return_401_unauthorized(self):
        url = reverse("product:product-api-detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_search_return_401_unauthorized(self):
        url = reverse("product:product-api-list") + "?search=Product"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_alert_return_401_unauthorized(self):
        url = reverse("product:product-api-alert-products")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_create_return_401_unauthorized(self):
        url = reverse("product:product-api-list")
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_update_return_401_unauthorized(self):
        url = reverse("product:product-api-list")
        response = self.client.put(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_partial_update_return_401_unauthorized(self):
        url = reverse("product:product-api-detail", args=(1,))
        response = self.client.patch(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_product_jwt_product_delete_return_401_unauthorized(self):
        url = reverse("product:product-api-detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
