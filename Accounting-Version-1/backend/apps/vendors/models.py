from django.db import models
from apps.accounts.models import Company

class Vendor(models.Model):
    VendorID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=255, null=True, blank=True)
    Phone = models.CharField(max_length=20, null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    PaymentTerms = models.CharField(max_length=50, null=True, blank=True)
    VendorNotes = models.TextField(null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'Vendors'
