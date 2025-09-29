from django.db import models
from apps.accounts.models import Company

class Integration(models.Model):
    IntegrationID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    IntegrationType = models.CharField(max_length=100)
    APIKey = models.CharField(max_length=255)
    Settings = models.JSONField(null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Integrations'

    def __str__(self):
        return f"Integration {self.IntegrationID} ({self.IntegrationType})"
