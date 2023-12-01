from .. import models


def create_log_product(product):
    log_product = models.LogProduct.objects.create(
        name=product.get('name', 'Sem nome'),
        description=product.get(
            'description', 'Esse produto não possui uma descrição'
        ),
        brand=product.get('brand', 'Sem marca'),
        quantity=product.get('quantity', 1),
        price=product.get('price', 1),
    )

    return log_product


def product_is_different(product):
    log_product = models.LogProduct.objects.filter(
        name=product.get('name')
    ).first()

    if log_product:
        if product.get('description') != log_product.description:
            return True

        if product.get('brand') != log_product.brand:
            return True

        if product.get('quantity') != log_product.quantity:
            return True

        if product.get('price') != log_product.price:
            return True

        return False
    else:
        return True


def analyze_product_save(instance, products):
    for product in products:
        if product_is_different(product):
            log_product = create_log_product(product)
            instance.log_products.add(log_product)
        else:
            log_product = models.LogProduct.objects.filter(
                name=product.get('name'),
                description=product.get('description'),
                brand=product.get('brand'),
                quantity=product.get('quantity'),
                price=product.get('price')
            ).first()
            instance.log_products.add(log_product)
