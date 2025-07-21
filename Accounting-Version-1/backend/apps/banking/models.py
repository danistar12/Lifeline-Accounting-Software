from django.db import models
from apps.accounts.models import Company
from apps.core.models import GeneralLedger

class BankAccount(models.Model):
    bank_account_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BankAccounts'

class BankStatementLine(models.Model):
    statement_line_id = models.AutoField(primary_key=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BankStatementLines'

class ReconciliationEntry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    statement_line = models.ForeignKey(BankStatementLine, on_delete=models.CASCADE)
    gl_transaction = models.ForeignKey(GeneralLedger, on_delete=models.CASCADE)
    reconciled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ReconciliationEntries'
