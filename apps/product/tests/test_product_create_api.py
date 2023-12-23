from django.urls import reverse
from django.utils import timezone
from parameterized import parameterized
from rest_framework import status

from apps.utils import querys

from .base_product import BaseProductApiTest


class ProductCreateApiTest(BaseProductApiTest):
    def create_product_by_views(
        self, token, name='Product', description='Description',
        brand='Brand', quantity=10, purchase_price=10,
        sale_price=11, expiration=timezone.now().date()
    ):
        data = {
            'name': name,
            'description': description,
            'brand': brand,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'sale_price': sale_price,
            'expiration': expiration,
        }

        url = reverse('product:product-api-list')
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        return response

    def test_product_product_api_post_return_status_code_201_created(self):
        EXPIRATION = timezone.now().date()
        admin_data = {'username': 'Admin', 'password': 'Pass'}
        admin = self.create_super_user(**admin_data)

        data = {
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

        product = querys.get_product(name='Product')
        self.assertEqual(admin, product.company)

    @parameterized.expand([
        'name', 'description', 'brand', 'quantity',
        'purchase_price', 'sale_price'
    ])
    def test_product_product_api_post_cannot_be_blank(self, field):
        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data={})

        message = 'Este campo é obrigatório.'
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_can_be_blank(self):
        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data={})

        response_mesage = response.data.get('expiraton')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(response_mesage)

    def test_product_product_api_post_name_exist(self):
        admin_data = {'username': 'Admin', 'password': 'Pass'}
        admin = self.create_super_user(**admin_data)

        product = self.create_product(company=admin)
        data = {'name': product.name}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = 'product com este name já existe.'
        response_mesage = response.data.get('name')[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_quantity_invalid(self):
        field = 'quantity'
        data = {field: -1}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = 'Certifque-se de que este valor seja maior ou igual a 0.'
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_purchase_price_invalid(self):
        field = 'purchase_price'
        data = {field: -1}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = 'Certifque-se de que este valor seja maior ou igual a 0.0.'
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_sale_price_invalid(self):
        field = 'sale_price'
        data = {field: -1}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = 'Certifque-se de que este valor seja maior ou igual a 0.0.'
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_expiration_invalid_format(self):
        field = 'expiration'
        data = {field: '12-12-2300'}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = (
            'Formato inválido para data. Use um dos formatos '
            'a seguir: YYYY-MM-DD.'
        )
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_expiration_previous_date_invalid(self):
        EXPIRATION = (timezone.now() - timezone.timedelta(days=1)).date()

        field = 'expiration'
        data = {field: EXPIRATION}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = 'A data de validade deve ser posterior ao dia atual.'
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_expiration_later_date_invalid(self):
        EXPIRATION = '2023-12-32'

        field = 'expiration'
        data = {field: EXPIRATION}

        url = reverse('product:product-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = (
            'Formato inválido para data. Use um dos formatos '
            'a seguir: YYYY-MM-DD.'
        )
        response_mesage = response.data.get(field)[0]

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(message, response_mesage)

    def test_product_product_api_post_product_expiration_log_was_raised(self):
        token = self.get_jwt_token()
        response = self.create_product_by_views(token=token)

        name = response.data.get('name')
        product = querys.get_product(name=name)
        log_product = querys.get_product_expiration_log(product=product)

        self.assertTrue(log_product)

    def test_product_product_api_post_product_expiration_log_not_created(self):
        token = self.get_jwt_token()
        response = self.create_product_by_views(
            token=token,
            expiration='',
        )

        name = response.data.get('name')
        product = querys.get_product(name=name)
        log_product = querys.get_product_expiration_log(product=product)

        self.assertFalse(log_product)
