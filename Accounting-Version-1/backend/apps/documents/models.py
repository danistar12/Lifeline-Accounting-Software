from django.db import models
from apps.accounts.models import Company

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    file_name = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey('core.Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    bill = models.ForeignKey('core.Bill', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('core.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey('core.Vendor', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Documents'
