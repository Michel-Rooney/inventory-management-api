import json

from django.urls import reverse

from apps.utils import querys
from .base_purchase import BasePurchaseApiTest


class PurchaseCreateApiTest(BasePurchaseApiTest):
    # [ X ] TODO: verificar se o cara ta logado
    # [ X ] TODO: verificar os status que ele não pode usar
    # [ X ] TODO: verificar as validações da criação
    # [ X ] TODO: verificar se os dados dos produtos são iguais
    # [ X ] TODO: verificar se o produto com esse nome existe
    # [ X ] TODO: verificar se criou o log de compras
    # [ X ] TODO: verificar se descontou a quantidade do log de compras
    # TODO: verificar se quando realiza nova compra faz a referencia para o produto correto  # noqa: E501
    # TODO: verificar se quando atualiza ajusta a quantidade de log de produtos

    def test_purchase_api_post_product_log_created(self):
        admin_data = {'username': 'Admin', 'password': 'Pass'}
        admin = self.create_super_user(**admin_data)

        product = self.create_product(company=admin)

        data = {
            'total_price': 20,
            'products': [
                {
                    'name': product.name,
                    'description': product.description,
                    'brand': product.brand,
                    'quantity': 1,
                    'purchase_price': product.purchase_price,
                    'sale_price': product.sale_price,
                    'expiration': product.expiration,
                }
            ]
        }

        json_data = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token(**admin_data, create_user=False)

        self.client.post(
            url, data=json_data,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        product_log = querys.get_log_products(
            name=product.name
        )

        self.assertTrue(product_log)

    def test_purchase_api_post_discounted_from_quantity(self):
        QUANTITY = 2
        admin_data = {'username': 'Admin', 'password': 'Pass'}
        admin = self.create_super_user(**admin_data)

        product = self.create_product(company=admin)
        DIFF = product.quantity - QUANTITY

        data = {
            'total_price': 20,
            'products': [
                {
                    'name': product.name,
                    'description': product.description,
                    'brand': product.brand,
                    'quantity': QUANTITY,
                    'purchase_price': product.purchase_price,
                    'sale_price': product.sale_price,
                    'expiration': product.expiration,
                }
            ]
        }

        json_data = json.dumps(data)

        url = reverse('purchase:purchase-api-list')
        token = self.get_jwt_token(**admin_data, create_user=False)

        self.client.post(
            url, data=json_data,
            HTTP_AUTHORIZATION=token,
            content_type='application/json'
        )

        actual_product = querys.get_product(name=product.name)
        self.assertEqual(DIFF, actual_product.quantity)
