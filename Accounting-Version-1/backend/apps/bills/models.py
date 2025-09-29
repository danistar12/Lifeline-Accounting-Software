from django.db import models
from apps.accounts.models import Company, User
from apps.vendors.models import Vendor

class Bill(models.Model):
    BillID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    VendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    BillNumber = models.CharField(max_length=50)
    BillDate = models.DateField()
    DueDate = models.DateField()
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2)
    Status = models.CharField(max_length=20)
    BillNotes = models.TextField(null=True, blank=True)
    CurrencyCode = models.CharField(max_length=3, default='USD')
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UserID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bill {self.BillNumber} - {self.VendorID.Name}"

    class Meta:
        db_table = 'Bills'
