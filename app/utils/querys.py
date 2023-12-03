from app import models


def get_purchases(**kwargs):
    purchases = models.Purchase.objects.filter(
        **kwargs
    ).select_related(
        'company'
    ).prefetch_related(
        'log_products'
    )

    return purchases


def get_purchase(**kwargs):
    purchase = models.Purchase.objects.filter(
        **kwargs
    ).select_related(
        'company'
    ).prefetch_related(
        'log_products'
    ).first()

    return purchase


def get_log_products(**kwargs):
    log_products = models.LogProduct.objects.filter(**kwargs)

    return log_products


def get_log_product(**kwargs):
    log_product = models.LogProduct.objects.filter(
        **kwargs
    ).first()

    return log_product


def get_products(**kwargs):
    products = models.Product.objects.filter(
        **kwargs
    ).select_related(
        'company'
    )

    return products


def get_product(**kwargs):
    product = models.Product.objects.filter(
        **kwargs
    ).select_related(
        'company'
    ).first()

    return product
