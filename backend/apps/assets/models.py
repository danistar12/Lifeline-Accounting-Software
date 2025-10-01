from django.db import models
from apps.accounts.models import Company

class FixedAsset(models.Model):
    AssetID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    AssetName = models.CharField(max_length=200)
    AssetTagNumber = models.CharField(max_length=100, null=True, blank=True)
    PurchaseDate = models.DateField()
    PurchaseCost = models.DecimalField(max_digits=18, decimal_places=2)
    DepreciationMethod = models.CharField(max_length=50)
    UsefulLifeYears = models.IntegerField()
    AssetNotes = models.TextField(null=True, blank=True)
    CurrentValue = models.DecimalField(max_digits=18, decimal_places=2)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    DisposalDate = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'FixedAssets'

    def __str__(self):
        return self.AssetName
