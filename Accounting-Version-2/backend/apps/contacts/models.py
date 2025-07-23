from django.db import models
from apps.core.models import Company

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
