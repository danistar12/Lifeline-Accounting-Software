from django.db import models
from apps.accounts.models import Company
from apps.invoices.models import Invoice
from apps.bills.models import Bill
from apps.customers.models import Customer
from apps.vendors.models import Vendor

class Document(models.Model):
    DocumentID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    FilePath = models.CharField(max_length=255)
    FileName = models.CharField(max_length=100)
    UploadDate = models.DateTimeField(auto_now_add=True)
    InvoiceID = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    BillID = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True)
    CustomerID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    VendorID = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.FileName

    class Meta:
        db_table = 'Documents'
