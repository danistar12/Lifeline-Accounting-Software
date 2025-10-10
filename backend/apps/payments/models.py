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

    PaymentID = models.AutoField(primary_key=True, verbose_name="Payment ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    InvoiceID = models.ForeignKey('invoices.Invoice', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Invoice")
    BillID = models.ForeignKey('bills.Bill', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bill")
    PaymentDate = models.DateField(verbose_name="Payment Date")
    Amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Amount")
    PaymentMethod = models.CharField(max_length=50, null=True, blank=True, verbose_name="Payment Method")
    PaymentNotes = models.TextField(null=True, blank=True, verbose_name="Payment Notes")
    CurrencyCode = models.CharField(max_length=3, default='USD', verbose_name="Currency Code")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    UserID = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")

    class Meta:
        db_table = 'Payments'
        ordering = ['-PaymentDate']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.PaymentID} - ${self.Amount}"