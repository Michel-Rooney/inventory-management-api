from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    company = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=64)
    description = models.CharField(
        max_length=255, default='Esse produto não possui uma descrição'
    )
    brand = models.CharField(
        max_length=64, default='Sem marca'
    )
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class LogProduct(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(
        max_length=255, default='Esse produto não possui uma descrição'
    )
    brand = models.CharField(
        max_length=64, default='Sem marca'
    )
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Purchase(models.Model):
    company = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True
    )
    total_price = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(LogProduct)
