from django.db import models
from apps.accounts.models import Company, User

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'Customers'

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'Vendors'

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Invoices'

class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Bills'

class ChartOfAccount(models.Model):
    account_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_code = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)
    account_notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ChartOfAccounts'
        unique_together = (('company', 'account_code'),)

class GeneralLedger(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    description = models.CharField(max_length=200, null=True, blank=True)
    debit_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    credit_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    gl_notes = models.TextField(null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='USD')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1.000000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'GeneralLedger'
