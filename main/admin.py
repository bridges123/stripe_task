from django.contrib import admin

from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'id']
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'order', 'quantity', 'id']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'is_active']
    search_fields = ['code', 'name']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['id', 'name']