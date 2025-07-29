from django.db import models
from apps.core.models import Company
from apps.core.models import Invoice, Bill

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    cost_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    inventory_notes = models.TextField(null=True, blank=True)
    valuation_method = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey('inventory.InventoryLocation', on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Inventory'

class InventoryLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'InventoryLocations'

class InvoiceLineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'InvoiceLineItems'

class BillLineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BillLineItems'
