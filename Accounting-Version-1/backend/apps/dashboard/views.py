from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DashboardMetric
from .serializers import DashboardMetricSerializer
from ..accounts.models import UserCompanyRole


class DashboardMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows dashboard metrics for the current user's companies to be viewed.
    """
    serializer_class = DashboardMetricSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter metrics for companies the user has access to
        user_companies = UserCompanyRole.objects.filter(UserID=user).values_list('CompanyID', flat=True)
        return DashboardMetric.objects.filter(CompanyID__in=user_companies)
