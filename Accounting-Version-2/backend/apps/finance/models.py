from django.db import models
from apps.core.models import Company, ChartOfAccounts

class ExchangeRate(models.Model):
    exchange_rate_id = models.AutoField(primary_key=True, db_column='ExchangeRateID')
    from_currency = models.CharField(max_length=3, db_column='FromCurrency')
    to_currency = models.CharField(max_length=3, db_column='ToCurrency')
    rate = models.DecimalField(max_digits=15, decimal_places=6, db_column='Rate')
    effective_date = models.DateField(db_column='EffectiveDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency}: {self.rate}"

    class Meta:
        db_table = 'ExchangeRates'

class FixedAsset(models.Model):
    asset_id = models.AutoField(primary_key=True, db_column='AssetID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    asset_name = models.CharField(max_length=255, db_column='AssetName')
    asset_tag_number = models.CharField(max_length=50, blank=True, null=True, db_column='AssetTagNumber')
    purchase_date = models.DateField(db_column='PurchaseDate')
    purchase_cost = models.DecimalField(max_digits=15, decimal_places=2, db_column='PurchaseCost')
    depreciation_method = models.CharField(max_length=50, db_column='DepreciationMethod')  # e.g., 'Straight Line', 'Declining Balance'
    useful_life_years = models.IntegerField(db_column='UsefulLifeYears')
    asset_notes = models.TextField(blank=True, null=True, db_column='AssetNotes')
    current_value = models.DecimalField(max_digits=15, decimal_places=2, db_column='CurrentValue')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    disposal_date = models.DateField(null=True, blank=True, db_column='DisposalDate')

    def __str__(self):
        return self.asset_name

    class Meta:
        db_table = 'FixedAssets'

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
