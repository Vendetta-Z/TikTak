from django.contrib import admin
from .models import Product


class AdminProduct(admin.ModelAdmin):
    list_display = ('Product_name', 'product_description', 'Product_price')
    search_fields = ['Product_name']




admin.site.register(Product, AdminProduct)

