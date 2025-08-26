from django.db import models
from apps.accounts.models import Company
from apps.core.models import GeneralLedger

class BankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)
    bank_acct_notes = models.TextField(null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='USD')
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

    class Meta:
        db_table = 'BankAccounts'

class BankTransaction(models.Model):
    bank_transaction_id = models.AutoField(primary_key=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    transaction_number = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    reconciled = models.BooleanField(default=False)
    general_ledger = models.ForeignKey(GeneralLedger, on_delete=models.SET_NULL, null=True, blank=True)
    is_imported = models.BooleanField(default=False)
    match_status = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - ${self.amount}"

    class Meta:
        db_table = 'BankTransactions'
