from django.db import models
from apps.core.models import Company
from apps.contacts.models import Customer, Vendor
from apps.accounts.models import User
from apps.inventory.models import Inventory

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True, db_column='InvoiceID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='CustomerID')
    invoice_number = models.CharField(max_length=50, db_column='InvoiceNumber')
    invoice_date = models.DateTimeField(db_column='InvoiceDate')
    due_date = models.DateTimeField(db_column='DueDate')
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAmount')
    status = models.CharField(max_length=20, default='Draft', db_column='Status')
    invoice_notes = models.TextField(blank=True, null=True, db_column='InvoiceNotes')
    currency_code = models.CharField(max_length=3, default='USD', db_column='CurrencyCode')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='UserID')
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"

    class Meta:
        db_table = 'Invoices'
        unique_together = ('company', 'invoice_number')

class InvoiceLineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True, db_column='LineItemID')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_column='InvoiceID')
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True, db_column='InventoryID')
    description = models.CharField(max_length=200, blank=True, null=True, db_column='Description')
    quantity = models.IntegerField(db_column='Quantity')
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, db_column='UnitPrice')
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAmount')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"

    class Meta:
        db_table = 'InvoiceLineItems'

class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True, db_column='BillID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column='VendorID')
    bill_number = models.CharField(max_length=50, db_column='BillNumber')
    bill_date = models.DateTimeField(db_column='BillDate')
    due_date = models.DateTimeField(db_column='DueDate')
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAmount')
    status = models.CharField(max_length=20, default='Pending', db_column='Status')
    bill_notes = models.TextField(blank=True, null=True, db_column='BillNotes')
    currency_code = models.CharField(max_length=3, default='USD', db_column='CurrencyCode')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='UserID')
    
    def __str__(self):
        return f"{self.bill_number} - {self.vendor.name}"

    class Meta:
        db_table = 'Bills'
        unique_together = ('company', 'bill_number')

class BillLineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True, db_column='LineItemID')
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, db_column='BillID')
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True, db_column='InventoryID')
    description = models.CharField(max_length=200, blank=True, null=True, db_column='Description')
    quantity = models.IntegerField(db_column='Quantity')
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, db_column='UnitPrice')
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAmount')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.bill.bill_number} - {self.description}"

    class Meta:
        db_table = 'BillLineItems'

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, db_column='PaymentID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, db_column='InvoiceID')
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, db_column='BillID')
    payment_date = models.DateTimeField(db_column='PaymentDate')
    amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='Amount')
    payment_method = models.CharField(max_length=50, blank=True, null=True, db_column='PaymentMethod')
    payment_notes = models.TextField(blank=True, null=True, db_column='PaymentNotes')
    currency_code = models.CharField(max_length=3, default='USD', db_column='CurrencyCode')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='UserID')
    
    def __str__(self):
        if self.invoice:
            return f"Payment for Invoice: {self.invoice.invoice_number}"
        elif self.bill:
            return f"Payment for Bill: {self.bill.bill_number}"
        else:
            return f"Payment: {self.payment_id}"

    class Meta:
        db_table = 'Payments'
