from django.db import models
from apps.accounts.models import Company
from apps.invoices.models import Invoice
from apps.bills.models import Bill
from apps.customers.models import Customer
from apps.vendors.models import Vendor

class Document(models.Model):
    DocumentID = models.AutoField(primary_key=True, verbose_name="Document ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    FilePath = models.CharField(max_length=255, verbose_name="File Path")
    FileName = models.CharField(max_length=100, verbose_name="File Name")
    UploadDate = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")
    InvoiceID = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Invoice")
    BillID = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bill")
    CustomerID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Customer")
    VendorID = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vendor")

    def __str__(self):
        return self.FileName

    class Meta:
        db_table = 'Documents'
        verbose_name = "Document"
        verbose_name_plural = "Documents"
