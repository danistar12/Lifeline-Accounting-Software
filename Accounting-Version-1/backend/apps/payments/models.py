from django.db import models
from apps.core.models import Company, Customer, Vendor, ChartOfAccount

class Payment(models.Model):
    PAYMENT_TYPES = [
        ('AP', 'Accounts Payable'),
        ('AR', 'Accounts Receivable'),
    ]

    payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPES)
    
    # Can be a customer (for AR) or null (for AP)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    
    # Can be a vendor (for AP) or null (for AR)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # The bank or cash account the payment is made from/to
    account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE, related_name='payments')
    
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Payments'
        ordering = ['-payment_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.payment_id} - {self.get_payment_type_display()}"