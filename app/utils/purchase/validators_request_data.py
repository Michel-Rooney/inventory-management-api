from rest_framework.validators import ValidationError


def name_validator(product, errors_product):
    name = product.get('name', '')

    if name == '':
        errors_product['name'] = ['O campo nome é obrigatório']

    return errors_product


def description_validator(product, errors_product):
    description = product.get('description', '')

    if description == '':
        errors_product['description'] = ['O campo de descrição é obrigatório']

    return errors_product


def brand_validator(product, errors_product):
    brand = product.get('brand', '')

    if brand == '':
        errors_product['brand'] = ['O campo de marca é obrigatório']

    return errors_product


def quantity_validator(product, errors_product):
    quantity = product.get('quantity', '')

    if quantity == '':
        errors_product['quantity'] = ['O campo de quantidade é obrigatório']
        return errors_product

    if quantity <= 0:
        errors_product['quantity'] = [
            'O campo de quantidade não pode ser negativo'
        ]

    return errors_product


def price_validator(product, errors_product):
    if product.get('price', '') == '':
        errors_product['price'] = ['O campo de preço é obrigatório']

    return errors_product


def analyze_request_data(products):
    errors = {}

    for i, product in enumerate(products, start=1):
        errors_product = {}

        product_name = product.get("name", f"Product {i}")
        product_name = f'Product {i}' if product_name == '' else product_name

        errors_product.update(name_validator(product, errors_product))
        errors_product.update(description_validator(product, errors_product))
        errors_product.update(brand_validator(product, errors_product))
        errors_product.update(quantity_validator(product, errors_product))
        errors_product.update(price_validator(product, errors_product))

        if errors_product:
            errors[f'{product_name}'] = errors_product

    if errors:
        raise ValidationError(errors)
