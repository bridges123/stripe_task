from django.contrib import admin


from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'id']