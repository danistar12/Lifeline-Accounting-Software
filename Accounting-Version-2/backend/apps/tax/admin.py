from django.contrib import admin
from .models import TaxRate, TaxTransaction

# Register your models here.
admin.site.register(TaxRate)
admin.site.register(TaxTransaction)
