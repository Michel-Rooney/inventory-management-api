import json

from django.urls import reverse

from .base_purchase import BasePurchaseApiTest


class PurchaseCreateEmptyValuesApiTest(BasePurchaseApiTest):
    def test_purchase_api_post_empty_total_price(self):
        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token)

        message = 'Este campo é obrigatório.'
        response_message = response.data.get('total_price')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_total_price_invalid(self):
        data = {
            "total_price": -1
        }

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        message = 'Certifque-se de que este valor seja maior ou igual a 0.0.'
        response_message = response.data.get('total_price')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_name(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo nome é obrigatório'
        response_message = response.data.get('Product 1').get('name')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_description(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de descrição é obrigatório'
        response_message = response.data.get('Product 1').get('description')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_brand(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de marca é obrigatório'
        response_message = response.data.get('Product 1').get('brand')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_quantity(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de quantidade é obrigatório'
        response_message = response.data.get('Product 1').get('quantity')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_quantity_invalid(self):
        data = {
            "total_price": 20.3,
            "products": [{
                'quantity': -1
            }]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de quantidade não pode ser negativo'
        response_message = response.data.get('Product 1').get('quantity')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_purchase_price(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de preço de compra é obrigatório'
        response_message = response.data.get(
            'Product 1'
        ).get('purchase_price')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_sale_price(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de preço de venda é obrigatório'
        response_message = response.data.get(
            'Product 1'
        ).get('sale_price')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_expiration(self):
        data = {
            "total_price": 20.3,
            "products": [{}]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'O campo de validade é obrigatório'
        response_message = response.data.get(
            'Product 1'
        ).get('expiration')[0]

        self.assertEqual(message, response_message)
