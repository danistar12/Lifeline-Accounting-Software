from django.contrib import admin
from .models import FixedAsset

@admin.register(FixedAsset)
class FixedAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'company', 'purchase_date', 'purchase_cost', 'current_value', 'depreciation_method')
    search_fields = ('asset_name', 'asset_tag_number', 'asset_notes')
    list_filter = ('depreciation_method', 'purchase_date', 'disposal_date')
    fieldsets = (
        ('Asset Information', {
            'fields': ('asset_name', 'asset_tag_number', 'company', 'asset_notes')
        }),
        ('Financial Details', {
            'fields': ('purchase_date', 'purchase_cost', 'depreciation_method', 'useful_life_years', 'current_value')
        }),
        ('Disposal', {
            'fields': ('disposal_date',)
        }),
    )
