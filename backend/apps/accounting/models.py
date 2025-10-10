from django.db import models
from apps.accounts.models import Company

class ChartOfAccount(models.Model):
    AccountID = models.AutoField(primary_key=True, verbose_name="Account ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    AccountCode = models.CharField(max_length=20, verbose_name="Account Code")
    AccountName = models.CharField(max_length=100, verbose_name="Account Name")
    AccountType = models.CharField(max_length=50, verbose_name="Account Type")
    AccountNotes = models.TextField(null=True, blank=True, verbose_name="Account Notes")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    IsActive = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.AccountCode} - {self.AccountName}"

    class Meta:
        db_table = 'ChartOfAccounts'
        verbose_name = "Chart of Account"
        verbose_name_plural = "Chart of Accounts"


class GeneralLedger(models.Model):
    TransactionID = models.AutoField(primary_key=True, verbose_name="Transaction ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    AccountID = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE, verbose_name="Account")
    TransactionDate = models.DateTimeField(verbose_name="Transaction Date")
    Description = models.CharField(max_length=200, null=True, blank=True, verbose_name="Description")
    DebitAmount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="Debit Amount")
    CreditAmount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="Credit Amount")
    GLNotes = models.TextField(null=True, blank=True, verbose_name="GL Notes")
    CurrencyCode = models.CharField(max_length=3, default='USD', verbose_name="Currency Code")
    ExchangeRate = models.DecimalField(max_digits=10, decimal_places=6, default=1.000000, verbose_name="Exchange Rate")
    UserID = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.TransactionDate} - {self.Description} - {self.AccountID.AccountName}"

    class Meta:
        db_table = 'GeneralLedger'
        verbose_name = "General Ledger Entry"
        verbose_name_plural = "General Ledger"
