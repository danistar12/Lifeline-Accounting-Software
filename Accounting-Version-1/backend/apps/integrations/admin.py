from django.contrib import admin
from .models import Integration

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('integration_id', 'company', 'integration_type', 'created_date')
    search_fields = ('integration_type',)
    list_filter = ('integration_type', 'created_date')
