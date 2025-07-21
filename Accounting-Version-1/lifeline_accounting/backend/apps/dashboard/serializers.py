from rest_framework import serializers
from .models import DashboardMetric


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = ['metric_id', 'name', 'value', 'updated_date']
