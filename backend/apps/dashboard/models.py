from django.db import models
from apps.accounts.models import Company

class DashboardMetric(models.Model):
    MetricID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Value = models.DecimalField(max_digits=18, decimal_places=2)
    UpdatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Name}: {self.Value}"

    class Meta:
        db_table = 'DashboardMetrics'
