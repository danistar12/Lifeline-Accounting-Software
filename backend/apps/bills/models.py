from django.db import models
from apps.accounts.models import Company, User
from apps.vendors.models import Vendor

class Bill(models.Model):
    BillID = models.AutoField(primary_key=True, verbose_name="Bill ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    VendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name="Vendor")
    BillNumber = models.CharField(max_length=50, verbose_name="Bill Number")
    BillDate = models.DateField(verbose_name="Bill Date")
    DueDate = models.DateField(verbose_name="Due Date")
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Total Amount")
    Status = models.CharField(max_length=20, verbose_name="Status")
    BillNotes = models.TextField(null=True, blank=True, verbose_name="Bill Notes")
    CurrencyCode = models.CharField(max_length=3, default='USD', verbose_name="Currency Code")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    UserID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name="Modified Date")

    def __str__(self):
        return f"Bill {self.BillNumber} - {self.VendorID.Name}"

    class Meta:
        db_table = 'Bills'
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
