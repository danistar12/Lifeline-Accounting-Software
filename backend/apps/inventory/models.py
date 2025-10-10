from django.db import models
from apps.accounts.models import Company
from apps.invoices.models import Invoice
from apps.bills.models import Bill

class Inventory(models.Model):
    InventoryID = models.AutoField(primary_key=True, verbose_name="Inventory ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    ProductCode = models.CharField(max_length=100, verbose_name="Product Code")
    ProductName = models.CharField(max_length=200, verbose_name="Product Name")
    Quantity = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Quantity")
    UnitPrice = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Unit Price")
    CostPrice = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Cost Price")
    InventoryNotes = models.TextField(null=True, blank=True, verbose_name="Inventory Notes")
    ValuationMethod = models.CharField(max_length=50, null=True, blank=True, verbose_name="Valuation Method")
    LocationID = models.ForeignKey('inventory.InventoryLocation', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Location")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.ProductCode} - {self.ProductName}"

    class Meta:
        db_table = 'Inventory'
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory"

class InventoryLocation(models.Model):
    LocationID = models.AutoField(primary_key=True, verbose_name="Location ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    LocationName = models.CharField(max_length=100, verbose_name="Location Name")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return self.LocationName

    class Meta:
        db_table = 'InventoryLocations'
        verbose_name = "Inventory Location"
        verbose_name_plural = "Inventory Locations"

class InvoiceLineItem(models.Model):
    LineItemID = models.AutoField(primary_key=True, verbose_name="Line Item ID")
    InvoiceID = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name="Invoice")
    InventoryID = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Inventory Item")
    Description = models.TextField(verbose_name="Description")
    Quantity = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Quantity")
    UnitPrice = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Unit Price")
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Total Amount")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"Invoice #{self.InvoiceID.InvoiceNumber} - {self.Description[:50]}"

    class Meta:
        db_table = 'InvoiceLineItems'
        verbose_name = "Invoice Line Item"
        verbose_name_plural = "Invoice Line Items"

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
