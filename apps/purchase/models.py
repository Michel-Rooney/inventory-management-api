from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from apps.product.models import ProductLog


class Purchase(models.Model):
    company = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    total_price = models.FloatField(validators=[MinValueValidator(0.00)])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    log_products = models.ManyToManyField(ProductLog, blank=True)

    def __str__(self) -> str:
        return f'Purchase {self.create_at}'
