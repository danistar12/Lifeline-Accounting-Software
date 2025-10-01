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
    
    AuditID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    ActionType = models.CharField(max_length=50, choices=ACTION_CHOICES, default=OTHER)
    ActionDescription = models.CharField(max_length=255)
    
    # Content type fields for generic relations
    ContentType = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    ObjectID = models.CharField(max_length=255, null=True, blank=True)
    ContentObject = GenericForeignKey('ContentType', 'ObjectID')
    
    # Legacy fields for backward compatibility
    Action = models.CharField(max_length=255, null=True, blank=True)
    TableName = models.CharField(max_length=100, null=True, blank=True, default="Unknown")
    RecordID = models.IntegerField(null=True, blank=True, default=0)
    
    # Data fields
    DataBefore = models.JSONField(null=True, blank=True)
    DataAfter = models.JSONField(null=True, blank=True)
    Details = models.TextField(null=True, blank=True)
    
    # Request data
    IPAddress = models.CharField(max_length=45, null=True, blank=True)
    UserAgent = models.TextField(null=True, blank=True)
    
    # Timestamps
    ActionDate = models.DateTimeField(default=now)
    
    class Meta:
        db_table = 'AuditLog'
        ordering = ['-ActionDate']

    def __str__(self):
        username = self.UserID.username if self.UserID else 'System'
        return f'{self.ActionDate} - {username} - {self.ActionDescription}'
