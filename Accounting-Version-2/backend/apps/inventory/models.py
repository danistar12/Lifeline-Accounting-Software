from django.db import models
from apps.core.models import Company

class InventoryLocation(models.Model):
    location_id = models.AutoField(primary_key=True, db_column='LocationID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    location_name = models.CharField(max_length=255, db_column='LocationName')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return self.location_name

    class Meta:
        db_table = 'InventoryLocations'

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True, db_column='InventoryID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    product_code = models.CharField(max_length=100, db_column='ProductCode')
    product_name = models.CharField(max_length=255, db_column='ProductName')
    quantity = models.IntegerField(db_column='Quantity')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='UnitPrice')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='CostPrice')
    inventory_notes = models.TextField(blank=True, null=True, db_column='InventoryNotes')
    valuation_method = models.CharField(max_length=50, db_column='ValuationMethod')  # e.g., 'FIFO', 'LIFO', 'Average'
    location = models.ForeignKey(InventoryLocation, on_delete=models.SET_NULL, null=True, blank=True, db_column='LocationID')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.product_code} - {self.product_name}"

    class Meta:
        db_table = 'Inventory'
        unique_together = ('company', 'product_code')
