from django.contrib import admin
from .models import Product, LogProduct, Purchase


admin.site.register(Product)
admin.site.register(LogProduct)
admin.site.register(Purchase)
