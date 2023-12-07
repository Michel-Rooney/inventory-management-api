from django.contrib import admin
from .models import Product, ProductLog, Purchase, ProductExpirationLog


admin.site.register(Product)
admin.site.register(ProductLog)
admin.site.register(Purchase)
admin.site.register(ProductExpirationLog)
