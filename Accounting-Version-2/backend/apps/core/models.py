from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    company_id = models.AutoField(primary_key=True, db_column='CompanyID')
    company_name = models.CharField(max_length=255, db_column='CompanyName')
    company_notes = models.TextField(blank=True, null=True, db_column='CompanyNotes')
    admin_user = models.ForeignKey('accounts.User', related_name='admin_of_companies', on_delete=models.SET_NULL, null=True, blank=True, db_column='AdminUserID')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'Companies'
        verbose_name_plural = "Companies"

# Customer model moved to apps.contacts.models

# Vendor model moved to apps.contacts.models

class ChartOfAccounts(models.Model):
    account_id = models.AutoField(primary_key=True, db_column='AccountID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    account_code = models.CharField(max_length=20, db_column='AccountCode')
    account_name = models.CharField(max_length=255, db_column='AccountName')
    account_type = models.CharField(max_length=50, db_column='AccountType')  # e.g., 'Asset', 'Liability', 'Equity', 'Revenue', 'Expense'
    account_notes = models.TextField(blank=True, null=True, db_column='AccountNotes')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    is_active = models.BooleanField(default=True, db_column='IsActive')

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"

    class Meta:
        db_table = 'ChartOfAccounts'
        unique_together = ('company', 'account_code')

class GeneralLedger(models.Model):
    transaction_id = models.AutoField(primary_key=True, db_column='TransactionID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE, db_column='AccountID')
    transaction_date = models.DateField(db_column='TransactionDate')
    description = models.TextField(db_column='Description')
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, db_column='DebitAmount')
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, db_column='CreditAmount')
    gl_notes = models.TextField(blank=True, null=True, db_column='GLNotes')
    currency_code = models.CharField(max_length=3, default='USD', db_column='CurrencyCode')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1.000000, db_column='ExchangeRate')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, db_column='UserID')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.transaction_date} - {self.description}"

    class Meta:
        db_table = 'GeneralLedger'

# Budget model moved to apps.finance.models

# FixedAsset model moved to apps.finance.models

# Project model moved to apps.project_tracking.models

# CustomField and CustomFieldValue models moved to apps.customization.models
