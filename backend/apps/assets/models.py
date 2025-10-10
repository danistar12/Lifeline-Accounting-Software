from django.db import models
from apps.accounts.models import Company

class FixedAsset(models.Model):
    AssetID = models.AutoField(primary_key=True, verbose_name="Asset ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    AssetName = models.CharField(max_length=200, verbose_name="Asset Name")
    AssetTagNumber = models.CharField(max_length=100, null=True, blank=True, verbose_name="Asset Tag Number")
    PurchaseDate = models.DateField(verbose_name="Purchase Date")
    PurchaseCost = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Purchase Cost")
    DepreciationMethod = models.CharField(max_length=50, verbose_name="Depreciation Method")
    UsefulLifeYears = models.IntegerField(verbose_name="Useful Life (Years)")
    AssetNotes = models.TextField(null=True, blank=True, verbose_name="Asset Notes")
    CurrentValue = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Current Value")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    DisposalDate = models.DateField(null=True, blank=True, verbose_name="Disposal Date")

    class Meta:
        db_table = 'FixedAssets'
        verbose_name = "Fixed Asset"
        verbose_name_plural = "Fixed Assets"

    def __str__(self):
        return self.AssetName
