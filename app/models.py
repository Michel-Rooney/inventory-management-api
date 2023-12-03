from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Product(models.Model):
    company = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=64)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0.00)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f'Log: {self.name} | {self.brand} | '
            f'Qtd: {self.quantity} | R$ {self.price}'
        )


class LogProduct(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=64)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField(validators=[MinValueValidator(0.00)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f'Log: {self.name} | {self.brand} | '
            f'Qtd: {self.quantity} | R$ {self.price}'
        )


class Purchase(models.Model):
    company = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    total_price = models.FloatField(validators=[MinValueValidator(0.00)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    log_products = models.ManyToManyField(LogProduct, blank=True)

    def __str__(self) -> str:
        return f'Purchase {self.create_at}'
