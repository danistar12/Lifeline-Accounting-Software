from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action_date', 'user', 'company', 'action', 'table_name', 'record_id')
    list_filter = ('action', 'company', 'action_date', 'user')
    search_fields = ('details', 'user__username', 'user__email', 'table_name')
    readonly_fields = (
        'user', 'company', 'action', 'table_name', 'record_id',
        'action_date', 'details'
    )
    date_hierarchy = 'action_date'
    
    def has_add_permission(self, request):
        # Audit logs should only be created through the application
        return False
    
    def has_change_permission(self, request, obj=None):
        # Audit logs should not be modified
        return False
