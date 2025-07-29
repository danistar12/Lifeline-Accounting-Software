from django.db import models
from apps.core.models import Company

class FixedAsset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=200)
    asset_tag_number = models.CharField(max_length=100, null=True, blank=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=18, decimal_places=2)
    depreciation_method = models.CharField(max_length=50)
    useful_life_years = models.IntegerField()
    asset_notes = models.TextField(null=True, blank=True)
    current_value = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    disposal_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'FixedAssets'

    def __str__(self):
        return self.asset_name
