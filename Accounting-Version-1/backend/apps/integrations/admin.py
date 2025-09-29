from django.contrib import admin
from .models import Integration

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('IntegrationID', 'CompanyID', 'IntegrationType', 'CreatedDate')
    search_fields = ('IntegrationType',)
    list_filter = ('IntegrationType', 'CreatedDate')
