from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name', 'quantity', 'last_scanned')
    search_fields = ('barcode', 'name')
