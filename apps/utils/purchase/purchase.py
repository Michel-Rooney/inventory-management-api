from apps.utils.purchase import validators, validators_request_data
from apps.utils.product.expiration import analyze_expiration
from apps.utils import querys


def create_purchase(self, serializer):
    products = self.request.data["products"]

    validators_request_data.analyze_request_data(products)
    validators.analyze_product_model_existence(products)

    company = self.request.user
    validators.analyze_product_save(serializer, company, products)

    total_price = 0
    total_purchase_price = 0

    for product in products:
        total_price += (
            product.get('quantity') * product.get('sale_price')
        )
        total_purchase_price += (
            product.get('quantity') * product.get('purchase_price')
        )

        instance = querys.get_product(name=product.get("name"))

        log_product_exits = querys.get_products_expiration_log(
            product=instance
        ).exists()

        if log_product_exits:
            quantity = instance.quantity - product.get("quantity", "")
            expiration = product.get("expiration", instance.expiration)
            analyze_expiration(instance, quantity, expiration)

    serializer.validated_data['total_price'] = total_price
    serializer.validated_data[
        'total_purchase_price'
    ] = total_purchase_price
