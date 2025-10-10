from django.db import models
from apps.accounts.models import Company, User
from apps.customers.models import Customer

class Invoice(models.Model):
    InvoiceID = models.AutoField(primary_key=True, verbose_name="Invoice ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    InvoiceNumber = models.CharField(max_length=50, verbose_name="Invoice Number")
    InvoiceDate = models.DateField(verbose_name="Invoice Date")
    DueDate = models.DateField(verbose_name="Due Date")
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Total Amount")
    Status = models.CharField(max_length=20, verbose_name="Status")
    InvoiceNotes = models.TextField(null=True, blank=True, verbose_name="Invoice Notes")
    CurrencyCode = models.CharField(max_length=3, default='USD', verbose_name="Currency Code")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    UserID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    SubscriptionID = models.ForeignKey('subscriptions.Subscription', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Subscription")

    def __str__(self):
        return f"Invoice {self.InvoiceNumber} - {self.CustomerID.Name}"

    class Meta:
        db_table = 'Invoices'
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
