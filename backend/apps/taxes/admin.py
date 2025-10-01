from django.contrib import admin
from .models import TaxRate, TaxTransaction

@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('TaxRateID', 'CompanyID', 'TaxName', 'Rate', 'Region', 'TaxRegime', 'EffectiveDate', 'CreatedDate')
    search_fields = ('TaxName', 'Region', 'TaxRegime')
    list_filter = ('EffectiveDate',)

@admin.register(TaxTransaction)
class TaxTransactionAdmin(admin.ModelAdmin):
    list_display = ('TaxTransactionID', 'CompanyID', 'InvoiceID', 'BillID', 'TaxRateID', 'TaxAmount', 'TransactionDate', 'CreatedDate')
    search_fields = ('TaxTransactionID',)
    list_filter = ('TransactionDate',)
