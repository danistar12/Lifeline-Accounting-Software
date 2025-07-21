from django.db import models
from apps.accounts.models import Company
from apps.core.models import Invoice

class ARPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ARPayments'

    def __str__(self):
        return f"ARPayment {self.payment_id} for Invoice {self.invoice.invoice_id}"
