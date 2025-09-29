from django.contrib import admin
from .models import ChartOfAccount, GeneralLedger

@admin.register(ChartOfAccount)
class ChartOfAccountAdmin(admin.ModelAdmin):
	list_display = ('AccountID', 'CompanyID', 'AccountCode', 'AccountName', 'AccountType', 'AccountNotes', 'CreatedDate', 'IsActive')
	search_fields = ('AccountCode', 'AccountName', 'AccountType')

@admin.register(GeneralLedger)
class GeneralLedgerAdmin(admin.ModelAdmin):
	list_display = ('TransactionID', 'CompanyID', 'AccountID', 'TransactionDate', 'Description', 'DebitAmount', 'CreditAmount', 'GLNotes', 'CurrencyCode', 'ExchangeRate', 'UserID', 'CreatedDate')
	search_fields = ('Description', 'CurrencyCode')
