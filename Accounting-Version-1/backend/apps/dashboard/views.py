from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DashboardMetric
from .serializers import DashboardMetricSerializer


class DashboardMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows dashboard metrics for the current user's companies to be viewed.
    """
    serializer_class = DashboardMetricSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter metrics for companies the user has access to
        return DashboardMetric.objects.filter(company__in=user.companies.all())
