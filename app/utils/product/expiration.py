from app.models import ProductExpirationLog


def analyze_expiration(before_expiration_model, serializer, diff_quantity):
    after_expiration_model = serializer.instance
    new_quantity = after_expiration_model.quantity

    print(before_expiration_model.expiration)
    print(after_expiration_model.expiration)
    if before_expiration_model.expiration != after_expiration_model.expiration:

        expiration_model = ProductExpirationLog.objects.filter(
            expiration=after_expiration_model.expiration
        ).first()

        if expiration_model:
            if diff_quantity <= 0:
                before_expiration_model.quantity += diff_quantity

                if before_expiration_model.quantity <= 0:
                    actual_expiration_model = ProductExpirationLog.objects.filter(
                        product__id=after_expiration_model.id
                    ).first()

                    actual_expiration_model.quantity += before_expiration_model.quantity
                    before_expiration_model.delete()

                else:
                    before_expiration_model.save()
            else:
                expiration_model.quantity += diff_quantity
                expiration_model.save()
        else:
            ProductExpirationLog.objects.create(
                product=after_expiration_model,
                quantity=diff_quantity,
                expiration=after_expiration_model.expiration
            )
    else:
        before_expiration_model.quantity = new_quantity
        before_expiration_model.save()
