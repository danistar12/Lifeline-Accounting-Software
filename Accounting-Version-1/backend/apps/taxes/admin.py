from django.contrib import admin
from .models import TaxRate, TaxTransaction

@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('tax_name', 'company', 'rate', 'region', 'effective_date')
    search_fields = ('tax_name', 'region', 'tax_regime')
    list_filter = ('effective_date',)

@admin.register(TaxTransaction)
class TaxTransactionAdmin(admin.ModelAdmin):
    list_display = ('tax_transaction_id', 'company', 'tax_rate', 'tax_amount', 'transaction_date')
    search_fields = ('tax_transaction_id',)
    list_filter = ('transaction_date',)
