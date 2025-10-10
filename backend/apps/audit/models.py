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
    
    AuditID = models.AutoField(primary_key=True, verbose_name="Audit ID")
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    ActionType = models.CharField(max_length=50, choices=ACTION_CHOICES, default=OTHER, verbose_name="Action Type")
    ActionDescription = models.CharField(max_length=255, verbose_name="Action Description")
    
    # Content type fields for generic relations
    ContentType = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Content Type")
    ObjectID = models.CharField(max_length=255, null=True, blank=True, verbose_name="Object ID")
    ContentObject = GenericForeignKey('ContentType', 'ObjectID')
    
    # Legacy fields for backward compatibility
    Action = models.CharField(max_length=255, null=True, blank=True, verbose_name="Action")
    TableName = models.CharField(max_length=100, null=True, blank=True, default="Unknown", verbose_name="Table Name")
    RecordID = models.IntegerField(null=True, blank=True, default=0, verbose_name="Record ID")
    
    # Data fields
    DataBefore = models.JSONField(null=True, blank=True, verbose_name="Data Before")
    DataAfter = models.JSONField(null=True, blank=True, verbose_name="Data After")
    Details = models.TextField(null=True, blank=True, verbose_name="Details")
    
    # Request data
    IPAddress = models.CharField(max_length=45, null=True, blank=True, verbose_name="IP Address")
    UserAgent = models.TextField(null=True, blank=True, verbose_name="User Agent")
    
    # Timestamps
    ActionDate = models.DateTimeField(default=now, verbose_name="Action Date")
    
    class Meta:
        db_table = 'AuditLog'
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Log"
        ordering = ['-ActionDate']

    def __str__(self):
        username = self.UserID.username if self.UserID else 'System'
        return f'{self.ActionDate} - {username} - {self.ActionDescription}'
