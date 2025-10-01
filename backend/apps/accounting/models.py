from django.db import models
from apps.accounts.models import Company

class ChartOfAccount(models.Model):
    AccountID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    AccountCode = models.CharField(max_length=20)
    AccountName = models.CharField(max_length=100)
    AccountType = models.CharField(max_length=50)
    AccountNotes = models.TextField(null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.AccountCode} - {self.AccountName}"

    class Meta:
        db_table = 'ChartOfAccounts'


class GeneralLedger(models.Model):
    TransactionID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    AccountID = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    TransactionDate = models.DateTimeField()
    Description = models.CharField(max_length=200, null=True, blank=True)
    DebitAmount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    CreditAmount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    GLNotes = models.TextField(null=True, blank=True)
    CurrencyCode = models.CharField(max_length=3, default='USD')
    ExchangeRate = models.DecimalField(max_digits=10, decimal_places=6, default=1.000000)
    UserID = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.TransactionDate} - {self.Description} - {self.AccountID.AccountName}"

    class Meta:
        db_table = 'GeneralLedger'
