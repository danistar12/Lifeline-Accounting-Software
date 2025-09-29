from django.db import models
from apps.accounts.models import Company, User
from apps.customers.models import Customer

class Invoice(models.Model):
    InvoiceID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    InvoiceNumber = models.CharField(max_length=50)
    InvoiceDate = models.DateField()
    DueDate = models.DateField()
    TotalAmount = models.DecimalField(max_digits=18, decimal_places=2)
    Status = models.CharField(max_length=20)
    InvoiceNotes = models.TextField(null=True, blank=True)
    CurrencyCode = models.CharField(max_length=3, default='USD')
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UserID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    SubscriptionID = models.ForeignKey('subscriptions.Subscription', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.InvoiceNumber} - {self.CustomerID.Name}"

    class Meta:
        db_table = 'Invoices'
