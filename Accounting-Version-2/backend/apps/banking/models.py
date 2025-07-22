from django.db import models
from apps.core.models import Company, GeneralLedger

class BankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True, db_column='BankAccountID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    account_number = models.CharField(max_length=50, db_column='AccountNumber')
    bank_name = models.CharField(max_length=255, db_column='BankName')
    account_type = models.CharField(max_length=50, db_column='AccountType')  # e.g., 'Checking', 'Savings'
    bank_acct_notes = models.TextField(blank=True, null=True, db_column='BankAcctNotes')
    currency_code = models.CharField(max_length=3, default='USD', db_column='CurrencyCode')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, db_column='Balance')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

    class Meta:
        db_table = 'BankAccounts'

class BankTransaction(models.Model):
    bank_transaction_id = models.AutoField(primary_key=True, db_column='BankTransactionID')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, db_column='BankAccountID')
    transaction_date = models.DateField(db_column='TransactionDate')
    transaction_number = models.CharField(max_length=100, blank=True, null=True, db_column='TransactionNumber')
    description = models.TextField(db_column='Description')
    amount = models.DecimalField(max_digits=15, decimal_places=2, db_column='Amount')
    transaction_type = models.CharField(max_length=50, db_column='TransactionType')  # e.g., 'Debit', 'Credit'
    reconciled = models.BooleanField(default=False, db_column='Reconciled')
    general_ledger = models.ForeignKey(GeneralLedger, on_delete=models.SET_NULL, null=True, blank=True, db_column='GeneralLedgerID')
    is_imported = models.BooleanField(default=False, db_column='IsImported')
    match_status = models.CharField(max_length=50, blank=True, null=True, db_column='MatchStatus')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.transaction_date} - {self.description}"

    class Meta:
        db_table = 'BankTransactions'
