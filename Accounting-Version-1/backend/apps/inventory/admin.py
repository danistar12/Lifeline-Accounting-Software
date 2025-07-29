from django.contrib import admin
from .models import Inventory, InventoryLocation, InvoiceLineItem, BillLineItem

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'product_name', 'quantity', 'unit_price')
    search_fields = ('product_code', 'product_name')
    list_filter = ('location',)

@admin.register(InventoryLocation)
class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = ('location_name',)
    search_fields = ('location_name',)

@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'total_amount')
    search_fields = ('description',)
    list_filter = ('created_date',)

@admin.register(BillLineItem)
class BillLineItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'description', 'quantity', 'unit_price', 'total_amount')
    search_fields = ('description',)
    list_filter = ('created_date',)
