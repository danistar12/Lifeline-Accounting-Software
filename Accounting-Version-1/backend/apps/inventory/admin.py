from django.contrib import admin
from .models import Inventory, InventoryLocation, InvoiceLineItem, BillLineItem

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('ProductCode', 'ProductName', 'Quantity', 'UnitPrice')
    search_fields = ('ProductCode', 'ProductName')
    list_filter = ('LocationID',)

@admin.register(InventoryLocation)
class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = ('LocationName',)
    search_fields = ('LocationName',)

@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    list_display = ('InvoiceID', 'Description', 'Quantity', 'UnitPrice', 'TotalAmount')
    search_fields = ('Description',)
    list_filter = ('CreatedDate',)

@admin.register(BillLineItem)
class BillLineItemAdmin(admin.ModelAdmin):
    list_display = ('BillID', 'Description', 'Quantity', 'UnitPrice', 'TotalAmount')
    search_fields = ('Description',)
    list_filter = ('CreatedDate',)
