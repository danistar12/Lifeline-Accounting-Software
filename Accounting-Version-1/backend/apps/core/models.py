from django.db import models
from django.utils.timezone import now
from apps.accounts.models import Company, User

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    payment_terms = models.CharField(max_length=50, null=True, blank=True)
    customer_notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Customers'

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    payment_terms = models.CharField(max_length=50, null=True, blank=True)
    vendor_notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Vendors'

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=20)
    invoice_notes = models.TextField(null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='USD')
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.name}"

    class Meta:
        db_table = 'Invoices'

class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=50)
    bill_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=20)
    bill_notes = models.TextField(null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='USD')
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Bill {self.bill_number} - {self.vendor.name}"

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

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"
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

class CustomField(models.Model):
    custom_field_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_custom_fields')
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50)
    table_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CustomFields'

class CustomFieldValue(models.Model):
    value_id = models.AutoField(primary_key=True)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE, related_name='core_custom_field_values')
    record_id = models.IntegerField()
    value = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CustomFieldValues'

class InvoiceLineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='core_invoice_line_items')
    inventory_id = models.IntegerField(default=0)
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreInvoiceLineItems'

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_inventory')
    product_code = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    cost_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    inventory_notes = models.TextField(null=True, blank=True)
    valuation_method = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey('inventory.InventoryLocation', on_delete=models.SET_NULL, null=True, blank=True, related_name='core_inventory')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreInventory'

class BillLineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='core_line_items')
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreBillLineItems'

class InventoryLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_inventory_locations')
    location_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreInventoryLocations'

class TimeEntry(models.Model):
    time_entry_id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='core_time_entries')
    employee_id = models.IntegerField()
    work_date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    time_entry_notes = models.TextField()
    billable = models.BooleanField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreTimeEntries'

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_projects')
    project_name = models.CharField(max_length=255, default='')
    customer_id = models.IntegerField(default=0)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    project_notes = models.TextField(default='')
    status = models.CharField(max_length=50, default='')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreProjects'

class AuditLog(models.Model):
    audit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_audit_logs')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_audit_logs')
    action = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255)
    record_id = models.IntegerField()
    action_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    class Meta:
        db_table = 'AuditLogs'

class UserCompanyRole(models.Model):
    user_company_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_user_company_roles')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_user_company_roles')
    role = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserCompanyRoles'

class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_budgets')
    account_id = models.IntegerField(default=0)
    description = models.TextField(default='')
    budget_year = models.IntegerField(default=now().year)
    budget_month = models.IntegerField(default=now().month)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    budget_notes = models.TextField(default='')
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_budgets', default=1)

    class Meta:
        db_table = 'CoreBudgets'

class FixedAsset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_fixed_assets')
    asset_name = models.CharField(max_length=200)
    asset_tag_number = models.CharField(max_length=100, null=True, blank=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=18, decimal_places=2)
    depreciation_method = models.CharField(max_length=50)
    useful_life_years = models.IntegerField()
    asset_notes = models.TextField(null=True, blank=True)
    current_value = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    disposal_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'CoreFixedAssets'

class Integration(models.Model):
    integration_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_integrations')
    integration_type = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255)
    settings = models.JSONField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreIntegrations'

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_payments')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='core_payments')
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, related_name='core_payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_notes = models.TextField(null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='USD')
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='core_payments')

    class Meta:
        db_table = 'CorePayments'

class TaxTransaction(models.Model):
    tax_transaction_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_tax_transactions')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='core_tax_transactions')
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, related_name='core_tax_transactions')
    tax_rate = models.ForeignKey('TaxRate', on_delete=models.CASCADE, related_name='core_transactions')
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2)
    transaction_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreTaxTransactions'

class TaxRate(models.Model):
    tax_rate_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='core_tax_rates')
    tax_name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    region = models.CharField(max_length=100, null=True, blank=True)
    tax_regime = models.CharField(max_length=100, null=True, blank=True)
    effective_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CoreTaxRates'

class ExchangeRate(models.Model):
    exchange_rate_id = models.AutoField(primary_key=True)
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=18, decimal_places=6)
    effective_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ExchangeRates'
        unique_together = (('from_currency', 'to_currency', 'effective_date'),)
