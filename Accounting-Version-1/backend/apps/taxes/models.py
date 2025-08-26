from django.db import models
from apps.core.models import Company, Invoice, Bill

class TaxRate(models.Model):
    tax_rate_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    region = models.CharField(max_length=100, null=True, blank=True)
    tax_regime = models.CharField(max_length=100, null=True, blank=True)
    effective_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tax_name} ({self.rate}%)"

    class Meta:
        db_table = 'TaxRates'

class TaxTransaction(models.Model):
    tax_transaction_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True)
    tax_rate = models.ForeignKey(TaxRate, on_delete=models.CASCADE)
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2)
    transaction_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.invoice:
            return f"Tax on Invoice #{self.invoice.invoice_number} - ${self.tax_amount}"
        elif self.bill:
            return f"Tax on Bill #{self.bill.bill_number} - ${self.tax_amount}"
        else:
            return f"Tax Transaction - ${self.tax_amount}"

    class Meta:
        db_table = 'TaxTransactions'
