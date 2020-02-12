from django.contrib import admin
from .models import Product, Order

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'stock_pcs', 'price', 'shop_id', 'vip')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'price', 'qty', 'shop_id')