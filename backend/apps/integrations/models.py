from django.db import models
from apps.accounts.models import Company

class Integration(models.Model):
    IntegrationID = models.AutoField(primary_key=True, verbose_name="Integration ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    IntegrationType = models.CharField(max_length=100, verbose_name="Integration Type")
    APIKey = models.CharField(max_length=255, verbose_name="API Key")
    Settings = models.JSONField(null=True, blank=True, verbose_name="Settings")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    class Meta:
        db_table = 'Integrations'
        verbose_name = "Integration"
        verbose_name_plural = "Integrations"

    def __str__(self):
        return f"Integration {self.IntegrationID} ({self.IntegrationType})"
