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

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, db_column='CustomerID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    name = models.CharField(max_length=255, db_column='Name')
    email = models.EmailField(blank=True, null=True, db_column='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    payment_terms = models.CharField(max_length=100, blank=True, null=True, db_column='PaymentTerms')
    customer_notes = models.TextField(blank=True, null=True, db_column='CustomerNotes')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Customers'

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True, db_column='VendorID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    name = models.CharField(max_length=255, db_column='Name')
    email = models.EmailField(blank=True, null=True, db_column='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    payment_terms = models.CharField(max_length=100, blank=True, null=True, db_column='PaymentTerms')
    vendor_notes = models.TextField(blank=True, null=True, db_column='VendorNotes')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Vendors'

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

class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True, db_column='BudgetID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE, db_column='AccountID')
    description = models.TextField(db_column='Description')
    budget_year = models.IntegerField(db_column='BudgetYear')
    budget_month = models.IntegerField(db_column='BudgetMonth')
    amount = models.DecimalField(max_digits=15, decimal_places=2, db_column='Amount')
    budget_notes = models.TextField(blank=True, null=True, db_column='BudgetNotes')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, db_column='UserID')

    def __str__(self):
        return f"{self.description} - {self.budget_year}/{self.budget_month}"

    class Meta:
        db_table = 'Budgets'

class FixedAsset(models.Model):
    asset_id = models.AutoField(primary_key=True, db_column='AssetID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    asset_name = models.CharField(max_length=255, db_column='AssetName')
    asset_tag_number = models.CharField(max_length=100, blank=True, null=True, db_column='AssetTagNumber')
    purchase_date = models.DateField(db_column='PurchaseDate')
    purchase_cost = models.DecimalField(max_digits=15, decimal_places=2, db_column='PurchaseCost')
    depreciation_method = models.CharField(max_length=50, db_column='DepreciationMethod')
    useful_life_years = models.IntegerField(db_column='UsefulLifeYears')
    asset_notes = models.TextField(blank=True, null=True, db_column='AssetNotes')
    current_value = models.DecimalField(max_digits=15, decimal_places=2, db_column='CurrentValue')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    disposal_date = models.DateField(blank=True, null=True, db_column='DisposalDate')

    def __str__(self):
        return self.asset_name

    class Meta:
        db_table = 'FixedAssets'

class Project(models.Model):
    project_id = models.AutoField(primary_key=True, db_column='ProjectID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    project_name = models.CharField(max_length=255, db_column='ProjectName')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='CustomerID')
    start_date = models.DateField(db_column='StartDate')
    end_date = models.DateField(blank=True, null=True, db_column='EndDate')
    budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, db_column='Budget')
    project_notes = models.TextField(blank=True, null=True, db_column='ProjectNotes')
    status = models.CharField(max_length=50, db_column='Status')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'Projects'

class CustomField(models.Model):
    custom_field_id = models.AutoField(primary_key=True, db_column='CustomFieldID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    field_name = models.CharField(max_length=255, db_column='FieldName')
    field_type = models.CharField(max_length=50, db_column='FieldType')  # e.g., 'text', 'number', 'date', 'boolean'
    table_name = models.CharField(max_length=100, db_column='TableName')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.table_name}.{self.field_name}"

    class Meta:
        db_table = 'CustomFields'

class CustomFieldValue(models.Model):
    value_id = models.AutoField(primary_key=True, db_column='ValueID')
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE, db_column='CustomFieldID')
    record_id = models.IntegerField(db_column='RecordID')
    value = models.TextField(db_column='Value')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.custom_field.field_name}: {self.value}"

    class Meta:
        db_table = 'CustomFieldValues'
