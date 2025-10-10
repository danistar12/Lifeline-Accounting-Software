from django.db import models
from apps.accounts.models import Company
from apps.invoices.models import Invoice
from apps.bills.models import Bill

class TaxRate(models.Model):
    TaxRateID = models.AutoField(primary_key=True, verbose_name="Tax Rate ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    TaxName = models.CharField(max_length=100, verbose_name="Tax Name")
    Rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Rate")
    Region = models.CharField(max_length=100, null=True, blank=True, verbose_name="Region")
    TaxRegime = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tax Regime")
    EffectiveDate = models.DateField(verbose_name="Effective Date")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.TaxName} ({self.Rate}%)"

    class Meta:
        db_table = 'TaxRates'
        verbose_name = "Tax Rate"
        verbose_name_plural = "Tax Rates"

class TaxTransaction(models.Model):
    TaxTransactionID = models.AutoField(primary_key=True, verbose_name="Tax Transaction ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    InvoiceID = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Invoice")
    BillID = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bill")
    TaxRateID = models.ForeignKey(TaxRate, on_delete=models.CASCADE, verbose_name="Tax Rate")
    TaxAmount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Tax Amount")
    TransactionDate = models.DateTimeField(verbose_name="Transaction Date")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        if self.InvoiceID:
            return f"Tax on Invoice #{self.InvoiceID.InvoiceNumber} - ${self.TaxAmount}"
        elif self.BillID:
            return f"Tax on Bill #{self.BillID.BillNumber} - ${self.TaxAmount}"
        else:
            return f"Tax Transaction - ${self.TaxAmount}"

    class Meta:
        db_table = 'TaxTransactions'
        verbose_name = "Tax Transaction"
        verbose_name_plural = "Tax Transactions"
