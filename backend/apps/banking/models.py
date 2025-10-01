from django.db import models
from decimal import Decimal
from apps.accounts.models import Company
from apps.accounting.models import GeneralLedger

class BankAccount(models.Model):
    BankAccountID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    AccountNumber = models.CharField(max_length=50)
    BankName = models.CharField(max_length=100)
    AccountType = models.CharField(max_length=50)
    BankAcctNotes = models.TextField(null=True, blank=True)
    CurrencyCode = models.CharField(max_length=3, default='USD')
    Balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.BankName} - {self.AccountNumber}"

    class Meta:
        db_table = 'BankAccounts'

class BankStatementLine(models.Model):
    BankStatementLineID = models.AutoField(primary_key=True)
    BankAccountID = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    TransactionDate = models.DateTimeField()
    TransactionNumber = models.CharField(max_length=100, null=True, blank=True)
    Description = models.CharField(max_length=255)
    Amount = models.DecimalField(max_digits=18, decimal_places=2)
    TransactionType = models.CharField(max_length=50)
    Reconciled = models.BooleanField(default=False)
    GeneralLedgerID = models.ForeignKey(GeneralLedger, on_delete=models.SET_NULL, null=True, blank=True)
    IsImported = models.BooleanField(default=False)
    MatchStatus = models.CharField(max_length=50, null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Description} - ${self.Amount}"

    class Meta:
        db_table = 'BankStatementLines'

class ReconciliationEntry(models.Model):
    ReconciliationEntryID = models.AutoField(primary_key=True)
    BankStatementLineID = models.ForeignKey(BankStatementLine, on_delete=models.CASCADE)
    GeneralLedgerID = models.ForeignKey(GeneralLedger, on_delete=models.CASCADE)
    ReconciledAmount = models.DecimalField(max_digits=18, decimal_places=2)
    ReconciledDate = models.DateTimeField(auto_now_add=True)
    Notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Reconciliation: {self.BankStatementLineID} - {self.GeneralLedgerID}"

    class Meta:
        db_table = 'ReconciliationEntries'
