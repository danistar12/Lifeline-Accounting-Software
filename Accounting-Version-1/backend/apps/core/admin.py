from django.contrib import admin
from .models import ChartOfAccount, GeneralLedger, Customer, Vendor, Invoice, Bill

admin.site.register(ChartOfAccount)
admin.site.register(GeneralLedger)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Invoice)
admin.site.register(Bill)
