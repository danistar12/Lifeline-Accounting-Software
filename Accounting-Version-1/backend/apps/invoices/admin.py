from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ('InvoiceID', 'CompanyID', 'CustomerID', 'InvoiceNumber', 'InvoiceDate', 'DueDate', 'TotalAmount', 'Status', 'CurrencyCode', 'UserID', 'SubscriptionID', 'CreatedDate')
	search_fields = ('InvoiceNumber', 'Status', 'CurrencyCode')
