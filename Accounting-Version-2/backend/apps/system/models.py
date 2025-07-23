from django.db import models
from apps.core.models import Company

class Integration(models.Model):
    integration_id = models.AutoField(primary_key=True, db_column='IntegrationID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    integration_type = models.CharField(max_length=100, db_column='IntegrationType')  # e.g., 'Banking', 'Payment Gateway', 'CRM'
    api_key = models.CharField(max_length=255, blank=True, null=True, db_column='APIKey')
    settings = models.TextField(blank=True, null=True, db_column='Settings')  # JSON or serialized settings
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.company.company_name} - {self.integration_type}"

    class Meta:
        db_table = 'Integrations'
