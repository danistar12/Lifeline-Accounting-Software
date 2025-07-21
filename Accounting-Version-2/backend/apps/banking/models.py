from django.db import models
from apps.core.models import Company
from apps.accounts.models import ChartOfAccounts

class BankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    chart_of_accounts_link = models.OneToOneField(ChartOfAccounts, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.account_name

class BankTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=50) # e.g., 'Debit', 'Credit'

    def __str__(self):
        return f"{self.transaction_date} - {self.description}"

class BankReconciliation(models.Model):
    reconciliation_id = models.AutoField(primary_key=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    statement_date = models.DateField()
    statement_balance = models.DecimalField(max_digits=15, decimal_places=2)
    reconciled_balance = models.DecimalField(max_digits=15, decimal_places=2)
    is_reconciled = models.BooleanField(default=False)

    def __str__(self):
        return f"Reconciliation for {self.bank_account.account_name} on {self.statement_date}"
