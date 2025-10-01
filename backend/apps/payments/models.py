from django.db import models
from apps.accounts.models import Company
from apps.customers.models import Customer
from apps.vendors.models import Vendor
from apps.accounting.models import ChartOfAccount

class Payment(models.Model):
    PAYMENT_TYPES = [
        ('AP', 'Accounts Payable'),
        ('AR', 'Accounts Receivable'),
    ]

    PaymentID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    InvoiceID = models.ForeignKey('invoices.Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    BillID = models.ForeignKey('bills.Bill', on_delete=models.SET_NULL, null=True, blank=True)
    PaymentDate = models.DateField()
    Amount = models.DecimalField(max_digits=18, decimal_places=2)
    PaymentMethod = models.CharField(max_length=50, null=True, blank=True)
    PaymentNotes = models.TextField(null=True, blank=True)
    CurrencyCode = models.CharField(max_length=3, default='USD')
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UserID = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Payments'
        ordering = ['-PaymentDate']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.PaymentID} - ${self.Amount}"