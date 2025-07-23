from django.db import models
from apps.core.models import Company
from apps.payments.models import Invoice, Bill

class TaxRate(models.Model):
    tax_rate_id = models.AutoField(primary_key=True, db_column='TaxRateID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    tax_name = models.CharField(max_length=100, db_column='TaxName')
    rate = models.DecimalField(max_digits=6, decimal_places=4, db_column='Rate')
    region = models.CharField(max_length=100, blank=True, null=True, db_column='Region')
    tax_regime = models.CharField(max_length=100, blank=True, null=True, db_column='TaxRegime')
    effective_date = models.DateField(db_column='EffectiveDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.tax_name} - {self.rate}%"

    class Meta:
        db_table = 'TaxRates'

class TaxTransaction(models.Model):
    tax_transaction_id = models.AutoField(primary_key=True, db_column='TaxTransactionID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, db_column='InvoiceID')
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, db_column='BillID')
    tax_rate = models.ForeignKey(TaxRate, on_delete=models.CASCADE, db_column='TaxRateID')
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, db_column='TaxAmount')
    transaction_date = models.DateField(db_column='TransactionDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        if self.invoice:
            return f"Tax on Invoice: {self.invoice.invoice_number}"
        elif self.bill:
            return f"Tax on Bill: {self.bill.bill_number}"
        else:
            return f"Tax Transaction: {self.tax_transaction_id}"

    class Meta:
        db_table = 'TaxTransactions'
