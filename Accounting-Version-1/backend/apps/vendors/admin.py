from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
	list_display = ('VendorID', 'CompanyID', 'Name', 'Email', 'Phone', 'Address', 'PaymentTerms', 'VendorNotes', 'CreatedDate')
	search_fields = ('Name', 'Email', 'Phone')
