from app.utils import querys


def analyze_expiration(self, serializer):
    # 1- Preciso pegar os dados da request
    instance = serializer.instance
    quantity = self.request.data.get('quantity', '')
    expiration = self.request.data.get(
        'expiration', str(instance.expiration)
    )

    if quantity == '':
        return True

    diff_quantity = quantity - instance.quantity

    # 2- Preciso pegar o antigo_model do ValidatyProduct
    # apartir do id e da data
    before_model = querys.get_product_expiration_log(
        product__id=instance.id,
        expiration=instance.expiration
    )

    # 3- Validar se o antigo_model realmente existe
    #     1. Se existir, passa a diante
    #     2. Se não existir, criar novo model apartir da diferença
    if not before_model:
        querys.create_product_expiration_log(
            product=instance,
            quantity=diff_quantity,
            expiration=instance.expiration
        )
        return True

    # 4- Preciso validar se datas são iguais/diferentes
    #   1. Se iguais, preciso analisar se a diferença é positiva ou negativa
    if expiration != str(before_model.expiration):
        #   1. Se a diferença é positiva, criar novo model
        if diff_quantity > 0:
            querys.create_product_expiration_log(
                product=instance,
                quantity=diff_quantity,
                expiration=expiration
            )

    #   2. Se a diferença é negativa, tirar do antigo_model
        else:
            before_model.quantity += diff_quantity
            before_model.save()

    #       1. Se o antigo_model ficar menor que 0, então deleta-lo
            if before_model.quantity == 0:
                before_model.delete()

            if before_model.quantity < 0:
                actual_model = querys.get_product_expiration_log(
                    product__id=instance.id,
                    expiration=expiration
                )

                actual_model += diff_quantity
                actual_model.save()

                before_model.delete()

    #     2. Se diferentes, preciso analisar se a diferença
    # é positva ou negativa
    else:
        #     1. Se a diferença é positiva, adicionar ao antigo_model
        if diff_quantity >= 0:
            before_model.quantity += diff_quantity
            before_model.save()

    #     2. Se a diferença negativa, tirar do antigo_model já existente
        else:
            befores_model = querys.get_products_expiration_log(
                product__id=instance.id
            )

            for i, model in enumerate(befores_model):
                model.quantity += diff_quantity
                model.save()

                if model.quantity == 0:
                    model.delete()

                if model.quantity < 0:
                    actual_model = befores_model[i]

                    print(f'{diff_quantity} | {actual_model.quantity}')
                    print(actual_model)

                    diff_quantity = model.quantity
                    actual_model.quantity += diff_quantity
                    actual_model.save()

                    print('after: ', diff_quantity)

                    model.delete()

                else:
                    break
