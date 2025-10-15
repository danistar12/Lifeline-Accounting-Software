from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import Company
from .models import Vendor
from .serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()

    def _company_queryset(self):
        return Company.objects.filter(usercompanyrole__UserID=self.request.user)

    def _get_active_company(self):
        companies = self._company_queryset()
        if not companies.exists():
            return None

        query_params = getattr(self.request, 'query_params', {})
        request_data = getattr(self.request, 'data', {})

        company_id = (
            self.request.headers.get('X-Company-ID')
            or query_params.get('CompanyID')
            or request_data.get('CompanyID')
        )

        if company_id:
            try:
                return companies.get(CompanyID=company_id)
            except (Company.DoesNotExist, ValueError):
                raise PermissionDenied("You do not have access to this company.")

        return companies.first()

    def get_queryset(self):
        company = self._get_active_company()
        if not company:
            return Vendor.objects.none()
        return Vendor.objects.filter(CompanyID=company)

    def perform_create(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        serializer.save(CompanyID=company)

    def perform_update(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        serializer.save(CompanyID=company)
