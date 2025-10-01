from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
	list_display = ('BillID', 'CompanyID', 'VendorID', 'BillNumber', 'BillDate', 'DueDate', 'TotalAmount', 'Status', 'CurrencyCode', 'UserID', 'CreatedDate', 'ModifiedDate')
	search_fields = ('BillNumber', 'Status', 'CurrencyCode')
