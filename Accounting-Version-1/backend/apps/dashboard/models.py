from django.db import models
from apps.accounts.models import Company

class DashboardMetric(models.Model):
    metric_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=18, decimal_places=2)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.value}"

    class Meta:
        db_table = 'DashboardMetrics'
