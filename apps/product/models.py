from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError(
            "A data de validade deve ser posterior ao dia atual."
        )


class Product(models.Model):
    company = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=64)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    purchase_price = models.FloatField(validators=[MinValueValidator(0.00)])
    sale_price = models.FloatField(validators=[MinValueValidator(0.00)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    expiration = models.DateField(
        validators=[validate_future_date], blank=True, null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return (
            f'{self.name} | {self.brand} | '
            f'Qtd: {self.quantity} | R$ {self.sale_price}'
        )


class ProductExpirationLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    expiration = models.DateField(validators=[validate_future_date])

    def __str__(self) -> str:
        return (
            f'{self.product.name} | Expiration: {self.expiration} |  '
            f'Qtd: {self.quantity}'
        )


class ProductLog(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=64)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    purchase_price = models.FloatField(validators=[MinValueValidator(0.00)])
    sale_price = models.FloatField(validators=[MinValueValidator(0.00)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    expiration = models.DateField(
        validators=[validate_future_date], blank=True, null=True
    )

    def __str__(self) -> str:
        return (
            f'Log: {self.name} | {self.brand} | '
            f'Qtd: {self.quantity} | R$ {self.sale_price}'
        )
