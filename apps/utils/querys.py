from apps.product.models import Product, ProductExpirationLog, ProductLog
from apps.purchase.models import Purchase


def get_purchases(**kwargs):
    purchases = Purchase.objects.filter(
        **kwargs
    ).select_related(
        'company'
    ).prefetch_related(
        'log_products'
    )

    return purchases


def get_purchase(**kwargs):
    purchase = Purchase.objects.filter(
        **kwargs
    ).select_related(
        'company'
    ).prefetch_related(
        'log_products'
    ).first()

    return purchase


def get_log_products(**kwargs):
    log_products = ProductLog.objects.filter(**kwargs)

    return log_products


def get_log_product(**kwargs):
    log_product = ProductLog.objects.filter(
        **kwargs
    ).first()

    return log_product


def get_products(**kwargs):
    products = Product.objects.filter(
        **kwargs
    ).select_related(
        'company'
    )

    return products


def get_product(**kwargs):
    product = Product.objects.filter(
        **kwargs
    ).select_related(
        'company'
    ).first()

    return product


def get_product_expiration_log(**kwargs):
    product = ProductExpirationLog.objects.filter(
        **kwargs
    ).select_related(
        'product'
    ).first()

    return product


def get_products_expiration_log(**kwargs):
    product = ProductExpirationLog.objects.filter(
        **kwargs
    ).select_related(
        'product'
    )

    return product


def create_product_expiration_log(**kwargs):
    product = ProductExpirationLog.objects.create(
        **kwargs
    )

    return product
