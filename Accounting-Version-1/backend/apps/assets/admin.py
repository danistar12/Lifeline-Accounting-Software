from django.contrib import admin
from .models import FixedAsset

@admin.register(FixedAsset)
class FixedAssetAdmin(admin.ModelAdmin):
    list_display = ('AssetName', 'CompanyID', 'PurchaseDate', 'PurchaseCost', 'CurrentValue', 'DepreciationMethod')
    search_fields = ('AssetName', 'AssetTagNumber', 'AssetNotes')
    list_filter = ('DepreciationMethod', 'PurchaseDate', 'DisposalDate')
    fieldsets = (
        ('Asset Information', {
            'fields': ('AssetName', 'AssetTagNumber', 'CompanyID', 'AssetNotes')
        }),
        ('Financial Details', {
            'fields': ('PurchaseDate', 'PurchaseCost', 'DepreciationMethod', 'UsefulLifeYears', 'CurrentValue')
        }),
        ('Disposal', {
            'fields': ('DisposalDate',)
        }),
    )
