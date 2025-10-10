from django.db import models
from apps.accounts.models import Company

class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True, verbose_name="Customer ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    Name = models.CharField(max_length=200, verbose_name="Name")
    Email = models.EmailField(max_length=255, null=True, blank=True, verbose_name="Email")
    Phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone")
    Address = models.TextField(null=True, blank=True, verbose_name="Address")
    PaymentTerms = models.CharField(max_length=50, null=True, blank=True, verbose_name="Payment Terms")
    CustomerNotes = models.TextField(null=True, blank=True, verbose_name="Customer Notes")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'Customers'
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
