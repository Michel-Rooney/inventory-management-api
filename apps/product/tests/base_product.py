from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import test

from apps.product.models import Product


class BaseProductApiTest(test.APITestCase, TestCase):
    def create_super_user(self, username="admin", password="adminpass"):
        return User.objects.create_superuser(
            username=username,
            password=password,
        )

    def get_jwt_token(
            self, username="admin", password="adminpass", create_user=True
    ):
        data = {"username": username, "password": password}

        if create_user:
            self.create_super_user(**data)

        url = reverse("user:token_obtain_pair")
        response = self.client.post(url, data=data)

        access = response.data.get("access")
        bearer = f"Bearer {access}"

        return bearer

    def create_product(
        self,
        company,
        name="Product 01",
        description="Description 01",
        brand="Brand 01",
        quantity=10,
        purchase_price=10,
        sale_price=11,
        expiration="2024-12-12",
    ):
        return Product.objects.create(
            company=company,
            name=name,
            description=description,
            brand=brand,
            quantity=quantity,
            purchase_price=purchase_price,
            sale_price=sale_price,
            expiration=expiration,
        )

    def create_amost_product(self, quantity, company):
        for i in range(quantity):
            Product.objects.create(
                company=company,
                name=f"Product {i}",
                description=f"Description {i}",
                brand=f"Brand {i}",
                quantity=i,
                purchase_price=i,
                sale_price=i,
                expiration=f"2024-12-{i + 1}",
            )
