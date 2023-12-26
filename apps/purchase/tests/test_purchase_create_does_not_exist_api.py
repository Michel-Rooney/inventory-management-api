import json
from parameterized import parameterized

from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from .base_purchase import BasePurchaseApiTest


class PurchaseCreateDoesNotExistApiTest(BasePurchaseApiTest):
    # [ X ] TODO: verificar se o cara ta logado
    # [ X ] TODO: verificar os status que ele não pode usar
    # [ X ] TODO: verificar as validações da criação
    # [ X ] TODO: verificar se os dados dos produtos são iguais
    # [ X ] TODO: verificar se o produto com esse nome existe
    # TODO: verificar se criou o log de compras
    # TODO: verificar se descontou a quantidade do log de compras
    # TODO: verificar se quando atualiza ajusta a quantidade de log de compras

    def test_purchase_api_post_title_does_not_exitst(self):
        NAME = 'Invalid Title'
        data = {
            'total_price': 10,
            'products': [
                {
                    'name': NAME,
                    'description': 'Description',
                    'brand': 'Brand',
                    'quantity': 10,
                    'purchase_price': 10,
                    'sale_price': 11,
                    'expiration': timezone.now().strftime("%Y-%m-%d")
                }
            ]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token()
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        message = 'Esse produto não existe'
        response_message = response.data.get(NAME)[0]

        self.assertEqual(message, response_message)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code) 

    @parameterized.expand([
        (
            'description',
            'O campo de descrição difere do produto escolhido.'
        ),
        (
            'quantity',
            'A quantidade exigida não possui estoque suficiente.'
        ),
        (
            'brand',
            'O campo de marca difere do produto escolhido.'
        ),
        (
            'purchase_price',
            'O campo de preço de compra difere do produto escolhido.'
        ),
        (
            'sale_price',
            'O campo de preço de venda difere do produto escolhido.'
        ),
        (
            'expiration',
            'O campo de validade difere do produto escolhido.'
        ),
    ])
    def test_purchase_api_post_fields_does_not_match(self, field, message):
        admin_data = {'username': 'Admin', 'password': 'Pass'}
        admin = self.create_super_user(**admin_data)

        product = self.create_product(company=admin)
        NAME = product.name

        EXPIRATION = (
            timezone.now() + timezone.timedelta(days=1)
        ).strftime("%Y-%m-%d")

        data = {
            'total_price': 10,
            'products': [
                {
                    'name': NAME,
                    'description': 'Description',
                    'brand': 'Brand',
                    'quantity': 99,
                    'purchase_price': 99,
                    'sale_price': 99,
                    'expiration': EXPIRATION,
                }
            ]
        }

        data_json = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token(**admin_data, create_user=False)
        response = self.client.post(
            url, data=data_json,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        response_message = response.data.get(NAME).get(field)[0]

        self.assertEqual(message, response_message)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
