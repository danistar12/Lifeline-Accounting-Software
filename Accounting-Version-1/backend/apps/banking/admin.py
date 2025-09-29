from django.contrib import admin
from .models import BankAccount, BankTransaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('BankAccountID', 'CompanyID', 'AccountNumber', 'BankName', 'AccountType', 'CurrencyCode', 'Balance', 'CreatedDate')
    search_fields = ('AccountNumber', 'BankName')
    list_filter = ('AccountType', 'CurrencyCode', 'CreatedDate')

@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('BankTransactionID', 'BankAccountID', 'TransactionDate', 'TransactionNumber', 'Description', 'Amount', 'TransactionType', 'Reconciled', 'GeneralLedgerID', 'IsImported', 'MatchStatus', 'CreatedDate')
    search_fields = ('TransactionNumber', 'Description')
    list_filter = ('TransactionType', 'Reconciled', 'IsImported', 'CreatedDate')
