from django.db import models
from apps.accounts.models import Company
from apps.invoices.models import Invoice
from apps.bills.models import Bill

class Inventory(models.Model):
    InventoryID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    ProductCode = models.CharField(max_length=100)
    ProductName = models.CharField(max_length=200)
    Quantity = models.DecimalField(max_digits=18, decimal_places=2)
    UnitPrice = models.DecimalField(max_digits=18, decimal_places=2)
    CostPrice = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    InventoryNotes = models.TextField(null=True, blank=True)
    ValuationMethod = models.CharField(max_length=50, null=True, blank=True)
    LocationID = models.ForeignKey('inventory.InventoryLocation', on_delete=models.SET_NULL, null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ProductCode} - {self.ProductName}"

    class Meta:
        db_table = 'Inventory'

class InventoryLocation(models.Model):
    LocationID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    LocationName = models.CharField(max_length=100)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.LocationName

    class Meta:
        db_table = 'InventoryLocations'

class InvoiceLineItem(models.Model):
    LineItemID = models.AutoField(primary_key=True)
    InvoiceID = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    InventoryID = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    Description = models.TextField()
    Quantity = models.DecimalField(max_digits=18, decimal_places=2)
    UnitPrice = models.DecimalField(max_digits=18, decimal_places=2)
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.InvoiceID.InvoiceNumber} - {self.Description[:50]}"

    class Meta:
        db_table = 'InvoiceLineItems'

class BillLineItem(models.Model):
    LineItemID = models.AutoField(primary_key=True)
    BillID = models.ForeignKey(Bill, on_delete=models.CASCADE)
    InventoryID = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    Description = models.TextField()
    Quantity = models.DecimalField(max_digits=18, decimal_places=2)
    UnitPrice = models.DecimalField(max_digits=18, decimal_places=2)
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.BillID.BillNumber} - {self.Description[:50]}"

    class Meta:
        db_table = 'BillLineItems'
