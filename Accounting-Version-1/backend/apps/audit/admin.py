from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('ActionDate', 'UserID', 'CompanyID', 'Action', 'TableName', 'RecordID')
    list_filter = ('Action', 'CompanyID', 'ActionDate', 'UserID')
    search_fields = ('Details', 'UserID__username', 'UserID__email', 'TableName')
    readonly_fields = (
        'UserID', 'CompanyID', 'Action', 'TableName', 'RecordID',
        'ActionDate', 'Details'
    )
    date_hierarchy = 'ActionDate'
    
    def has_add_permission(self, request):
        # Audit logs should only be created through the application
        return False
    
    def has_change_permission(self, request, obj=None):
        # Audit logs should not be modified
        return False
