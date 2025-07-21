from django.db import models
from apps.accounts.models import Company
from apps.core.models import Bill

class APPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'APPayments'

    def __str__(self):
        return f"APPayment {self.payment_id} for Bill {self.bill.bill_id}"
