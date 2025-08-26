from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from apps.accounts.models import Company

class AuditLog(models.Model):
    # Action types
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE = 'create'
    READ = 'read'
    VIEW = 'view'
    UPDATE = 'update'
    DELETE = 'delete'
    OTHER = 'other'
    
    ACTION_CHOICES = [
        (LOGIN, 'Login'),
        (LOGOUT, 'Logout'),
        (CREATE, 'Create'),
        (READ, 'Read'),
        (VIEW, 'View'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),
        (OTHER, 'Other'),
    ]
    
    audit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES, default=OTHER)
    action_description = models.CharField(max_length=255)
    
    # Content type fields for generic relations
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Legacy fields for backward compatibility
    action = models.CharField(max_length=255, null=True, blank=True)
    table_name = models.CharField(max_length=100, null=True, blank=True, default="Unknown")
    record_id = models.IntegerField(null=True, blank=True, default=0)
    
    # Data fields
    data_before = models.JSONField(null=True, blank=True)
    data_after = models.JSONField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    
    # Request data
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Timestamps
    action_date = models.DateTimeField(default=now)
    
    class Meta:
        db_table = 'AuditLog'
        ordering = ['-action_date']

    def __str__(self):
        username = self.user.username if self.user else 'System'
        return f'{self.action_date} - {username} - {self.action_description}'
