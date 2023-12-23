from rest_framework.validators import ValidationError

from apps.purchase import models
from apps.utils import querys


def create_log_product(product):
    log_product = models.ProductLog.objects.create(
        name=product.get('name', 'Sem nome'),
        description=product.get(
            'description', 'Esse produto não possui uma descrição'
        ),
        brand=product.get('brand', 'Sem marca'),
        quantity=product.get('quantity', 1),
        purchase_price=product.get('purchase_price', 1),
        sale_price=product.get('sale_price', 1),
        expiration=product.get('expiration', 1),
    )

    return log_product


def product_is_different(product):
    log_product = querys.get_log_product(name=product.get('name'))

    if log_product:
        if product.get('description') != log_product.description:
            return True

        if product.get('brand') != log_product.brand:
            return True

        if product.get('quantity') != log_product.quantity:
            return True

        if product.get('purchase_price') != log_product.purchase_price:
            return True

        if product.get('sale_price') != log_product.sale_price:
            return True

        return False
    else:
        return True


def sub_product_quantity(product):
    product_model = querys.get_product(name=product.get('name'))

    product_model.quantity -= product.get('quantity')
    product_model.save()


def analyze_product_save(serializer, company, products):
    for product in products:
        if product_is_different(product):
            log_product = create_log_product(product)
        else:
            log_product = querys.get_log_product(
                name=product.get('name'),
                description=product.get('description'),
                brand=product.get('brand'),
                quantity=product.get('quantity'),
                purchase_price=product.get('purchase_price'),
                sale_price=product.get('sale_price'),
                expiration=product.get('expiration'),
            )

        instance = serializer.save(company=company)
        instance.log_products.add(log_product)
        sub_product_quantity(product)


def analyze_product_model_existence(products):
    errors = {}

    for i, product in enumerate(products, start=1):
        erros_product = {}

        product_name = product.get("name", f"Product {i}")
        product_name = f'Product {i}' if product_name == '' else product_name

        product_model = querys.get_product(name=product.get('name'))

        if not product_model:
            raise ValidationError({
                f'{product_name}': ['Esse produto não existe']
            })

        if product.get('quantity') > product_model.quantity:
            raise ValidationError({
                f'{product_name}': [
                    'A quantidade exigida não possui estoque suficiente'
                ]
            })

        if product.get('name') != product_model.name:
            erros_product['name'] = [
                'O campo nome difere do produto escolhido'
            ]

        if product.get('description', '') != product_model.description:
            erros_product['description'] = [
                'O campo de descrição difere do produto escolhido'
            ]

        if product.get('brand', '') != product_model.brand:
            erros_product['brand'] = [
                'O campo de marca difere do produto escolhido'
            ]

        if product.get('purchase_price', '') != product_model.purchase_price:
            erros_product['purchase_price'] = [
                'O campo de preço de compra difere do produto escolhido'
            ]

        if product.get('sale_price', '') != product_model.sale_price:
            erros_product['sale_price'] = [
                'O campo de preço de venda difere do produto escolhido'
            ]

        if erros_product:
            errors[f'{product_name}'] = erros_product

    if errors:
        raise ValidationError(errors)
