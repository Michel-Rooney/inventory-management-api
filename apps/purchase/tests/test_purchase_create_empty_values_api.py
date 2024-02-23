import json

from django.urls import reverse

from .base_purchase import BasePurchaseApiTest


class PurchaseCreateEmptyValuesApiTest(BasePurchaseApiTest):
    def test_purchase_api_post_empty_purchase_price(self):
        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()

        data = {"products": [{}]}
        data_json = json.dumps(data)

        response = self.client.post(
            url, HTTP_AUTHORIZATION=token, data=data_json,
            content_type='application/json'
        )

        print(response.data)
        message = 'O campo de preço de compra é obrigatório'
        response_message = response.data.get(
            'Product 1').get('purchase_price')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_sale_price(self):
        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()

        data = {"products": [{}]}
        data_json = json.dumps(data)

        response = self.client.post(
            url, HTTP_AUTHORIZATION=token, data=data_json,
            content_type='application/json'
        )

        print(response.data)
        message = 'O campo de preço de venda é obrigatório'
        response_message = response.data.get(
            'Product 1').get('sale_price')[0]

        self.assertEqual(message, response_message)

    def test_purchase_api_post_empty_product_name(self):
        data = {
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
