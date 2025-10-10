from django.db import models
from apps.accounts.models import Company

class DashboardMetric(models.Model):
    MetricID = models.AutoField(primary_key=True, verbose_name="Metric ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    Name = models.CharField(max_length=100, verbose_name="Name")
    Value = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Value")
    UpdatedDate = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return f"{self.Name}: {self.Value}"

    class Meta:
        db_table = 'DashboardMetrics'
        verbose_name = "Dashboard Metric"
        verbose_name_plural = "Dashboard Metrics"
