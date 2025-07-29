from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from apps.accounts.models import Company

class AuditLog(models.Model):
    audit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    table_name = models.CharField(max_length=100, null=True, blank=True, default="Unknown")
    record_id = models.IntegerField(null=True, blank=True, default=0)
    action_date = models.DateTimeField(default=now)
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'AuditLog'
        ordering = ['-action_date']

    def __str__(self):
        return f'{self.action_date} - {self.user.username} - {self.action}'
