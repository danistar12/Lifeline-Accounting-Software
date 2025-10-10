from django.db import models
from decimal import Decimal
from apps.accounts.models import Company
from apps.accounting.models import GeneralLedger

class BankAccount(models.Model):
    BankAccountID = models.AutoField(primary_key=True, verbose_name="Bank Account ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    AccountNumber = models.CharField(max_length=50, verbose_name="Account Number")
    BankName = models.CharField(max_length=100, verbose_name="Bank Name")
    AccountType = models.CharField(max_length=50, verbose_name="Account Type")
    BankAcctNotes = models.TextField(null=True, blank=True, verbose_name="Bank Account Notes")
    CurrencyCode = models.CharField(max_length=3, default='USD', verbose_name="Currency Code")
    Balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'), verbose_name="Balance")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.BankName} - {self.AccountNumber}"

    class Meta:
        db_table = 'BankAccounts'
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"

class BankStatementLine(models.Model):
    BankStatementLineID = models.AutoField(primary_key=True, verbose_name="Bank Statement Line ID")
    BankAccountID = models.ForeignKey(BankAccount, on_delete=models.CASCADE, verbose_name="Bank Account")
    TransactionDate = models.DateTimeField(verbose_name="Transaction Date")
    TransactionNumber = models.CharField(max_length=100, null=True, blank=True, verbose_name="Transaction Number")
    Description = models.CharField(max_length=255, verbose_name="Description")
    Amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Amount")
    TransactionType = models.CharField(max_length=50, verbose_name="Transaction Type")
    Reconciled = models.BooleanField(default=False, verbose_name="Reconciled")
    GeneralLedgerID = models.ForeignKey(GeneralLedger, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="General Ledger Entry")
    IsImported = models.BooleanField(default=False, verbose_name="Is Imported")
    MatchStatus = models.CharField(max_length=50, null=True, blank=True, verbose_name="Match Status")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.Description} - ${self.Amount}"

    class Meta:
        db_table = 'BankStatementLines'
        verbose_name = "Bank Statement Line"
        verbose_name_plural = "Bank Statement Lines"

class ReconciliationEntry(models.Model):
    ReconciliationEntryID = models.AutoField(primary_key=True, verbose_name="Reconciliation Entry ID")
    BankStatementLineID = models.ForeignKey(BankStatementLine, on_delete=models.CASCADE, verbose_name="Bank Statement Line")
    GeneralLedgerID = models.ForeignKey(GeneralLedger, on_delete=models.CASCADE, verbose_name="General Ledger Entry")
    ReconciledAmount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Reconciled Amount")
    ReconciledDate = models.DateTimeField(auto_now_add=True, verbose_name="Reconciled Date")
    Notes = models.TextField(null=True, blank=True, verbose_name="Notes")

    def __str__(self):
        return f"Reconciliation: {self.BankStatementLineID} - {self.GeneralLedgerID}"

    class Meta:
        db_table = 'ReconciliationEntries'
        verbose_name = "Reconciliation Entry"
        verbose_name_plural = "Reconciliation Entries"
