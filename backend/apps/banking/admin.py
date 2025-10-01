from django.contrib import admin
from .models import BankAccount, BankStatementLine, ReconciliationEntry

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('BankAccountID', 'CompanyID', 'AccountNumber', 'BankName', 'AccountType', 'CurrencyCode', 'Balance', 'CreatedDate')
    search_fields = ('AccountNumber', 'BankName')
    list_filter = ('AccountType', 'CurrencyCode', 'CreatedDate')

@admin.register(BankStatementLine)
class BankStatementLineAdmin(admin.ModelAdmin):
    list_display = ('BankStatementLineID', 'BankAccountID', 'TransactionDate', 'TransactionNumber', 'Description', 'Amount', 'TransactionType', 'Reconciled', 'GeneralLedgerID', 'IsImported', 'MatchStatus', 'CreatedDate')
    search_fields = ('TransactionNumber', 'Description')
    list_filter = ('TransactionType', 'Reconciled', 'IsImported', 'CreatedDate')

@admin.register(ReconciliationEntry)
class ReconciliationEntryAdmin(admin.ModelAdmin):
    list_display = ('ReconciliationEntryID', 'BankStatementLineID', 'GeneralLedgerID', 'ReconciledAmount', 'ReconciledDate')
    search_fields = ('BankStatementLineID__Description', 'GeneralLedgerID__Description')
    list_filter = ('ReconciledDate',)
