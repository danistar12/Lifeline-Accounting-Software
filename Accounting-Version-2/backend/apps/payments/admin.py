from django.contrib import admin
from .models import Invoice, InvoiceLineItem, Bill, BillLineItem, Payment

# Register your models here.
admin.site.register(Invoice)
admin.site.register(InvoiceLineItem)
admin.site.register(Bill)
admin.site.register(BillLineItem)
admin.site.register(Payment)
