from django.contrib import admin
from .models import Product, ProductLog, ProductExpirationLog


admin.site.register(Product)
admin.site.register(ProductLog)
admin.site.register(ProductExpirationLog)

