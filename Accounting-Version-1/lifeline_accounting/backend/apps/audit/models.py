from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import Company

class AuditLog(models.Model):
    """
    Tracks user actions across the system for security and accountability.
    
    This model records:
    - Who performed the action (user)
    - Which company the action belongs to
    - What action was performed
    - When the action occurred
    - What entity was affected (through content_type and object_id)
    - Additional details about the action
    """
    # Action types
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    LOGIN = 'login'
    LOGOUT = 'logout'
    VIEW = 'view'
    EXPORT = 'export'
    IMPORT = 'import'
    OTHER = 'other'
    
    ACTION_CHOICES = [
        (CREATE, 'Create'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),
        (LOGIN, 'Login'),
        (LOGOUT, 'Logout'),
        (VIEW, 'View'),
        (EXPORT, 'Export'),
        (IMPORT, 'Import'),
        (OTHER, 'Other'),
    ]
    
    # Who performed the action
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audit_logs'
    )
    
    # Which company this action belongs to
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    
    # What action was performed
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_description = models.CharField(max_length=255)
    
    # When the action occurred
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # What entity was affected (Generic Foreign Key)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    object_id = models.CharField(max_length=50, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional details
    data_before = models.JSONField(null=True, blank=True)
    data_after = models.JSONField(null=True, blank=True)
    details = models.TextField(blank=True, null=True)
    
    # Security information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['action_type']),
            models.Index(fields=['company', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else 'System'
        return f'{self.timestamp.strftime("%Y-%m-%d %H:%M:%S")} - {user_str} - {self.action_description}'
