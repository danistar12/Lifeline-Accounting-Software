from django.db import models
from apps.core.models import Company

class Integration(models.Model):
    integration_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    integration_type = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255)
    settings = models.JSONField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Integrations'

    def __str__(self):
        return f"Integration {self.integration_id} ({self.integration_type})"
