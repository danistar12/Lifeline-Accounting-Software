from django.db import models
from apps.accounts.models import Company
from apps.invoices.models import Invoice
from apps.bills.models import Bill

class TaxRate(models.Model):
    TaxRateID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    TaxName = models.CharField(max_length=100)
    Rate = models.DecimalField(max_digits=10, decimal_places=4)
    Region = models.CharField(max_length=100, null=True, blank=True)
    TaxRegime = models.CharField(max_length=100, null=True, blank=True)
    EffectiveDate = models.DateField()
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.TaxName} ({self.Rate}%)"

    class Meta:
        db_table = 'TaxRates'

class TaxTransaction(models.Model):
    TaxTransactionID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    InvoiceID = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    BillID = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True)
    TaxRateID = models.ForeignKey(TaxRate, on_delete=models.CASCADE)
    TaxAmount = models.DecimalField(max_digits=18, decimal_places=2)
    TransactionDate = models.DateTimeField()
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.InvoiceID:
            return f"Tax on Invoice #{self.InvoiceID.InvoiceNumber} - ${self.TaxAmount}"
        elif self.BillID:
            return f"Tax on Bill #{self.BillID.BillNumber} - ${self.TaxAmount}"
        else:
            return f"Tax Transaction - ${self.TaxAmount}"

    class Meta:
        db_table = 'TaxTransactions'
