from django.contrib import admin
from .models import DashboardMetric

@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Value', 'CompanyID', 'UpdatedDate')
    list_filter = ('CompanyID', 'UpdatedDate')
    search_fields = ('Name',)
    ordering = ('-UpdatedDate',)