from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'company', 'action_type', 'action_description', 'ip_address')
    list_filter = ('action_type', 'company', 'timestamp', 'user')
    search_fields = ('action_description', 'details', 'user__username', 'user__email', 'ip_address')
    readonly_fields = (
        'user', 'company', 'action_type', 'action_description', 'timestamp',
        'content_type', 'object_id', 'data_before', 'data_after',
        'details', 'ip_address', 'user_agent'
    )
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # Audit logs should only be created through the application
        return False
    
    def has_change_permission(self, request, obj=None):
        # Audit logs should not be modified
        return False
