from django.contrib import admin
from .models import Product, ImageGallery


class GalleryInline(admin.TabularInline):
    model = ImageGallery


class AdminProduct(admin.ModelAdmin):
    list_display = ('Product_name', 'product_description', 'Product_price')
    search_fields = ['Product_name']
    inlines = [GalleryInline]


admin.site.register(Product, AdminProduct)
