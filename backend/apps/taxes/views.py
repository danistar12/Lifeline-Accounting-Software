from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import Company
from .models import TaxRate, TaxTransaction
from .serializers import TaxRateSerializer, TaxTransactionSerializer


class _CompanyScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

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
        queryset = super().get_queryset()
        company = self._get_active_company()
        if not company:
            return queryset.none()
        return queryset.filter(CompanyID=company)

    def _save_with_company(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        serializer.save(CompanyID=company)

    def perform_create(self, serializer):
        self._save_with_company(serializer)

    def perform_update(self, serializer):
        self._save_with_company(serializer)


class TaxRateViewSet(_CompanyScopedViewSet):
    serializer_class = TaxRateSerializer
    queryset = TaxRate.objects.all()


class TaxTransactionViewSet(_CompanyScopedViewSet):
    serializer_class = TaxTransactionSerializer
    queryset = TaxTransaction.objects.select_related('TaxRateID', 'InvoiceID', 'BillID')

    def _validate_relationships(self, serializer, company):
        tax_rate = serializer.validated_data.get('TaxRateID')
        if tax_rate and tax_rate.CompanyID_id != company.CompanyID:
            raise PermissionDenied("Tax rate does not belong to the selected company.")

        invoice = serializer.validated_data.get('InvoiceID')
        if invoice and getattr(invoice, 'CompanyID_id', None) != company.CompanyID:
            raise PermissionDenied("Invoice does not belong to the selected company.")

        bill = serializer.validated_data.get('BillID')
        if bill and getattr(bill, 'CompanyID_id', None) != company.CompanyID:
            raise PermissionDenied("Bill does not belong to the selected company.")

    def perform_create(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        self._validate_relationships(serializer, company)
        serializer.save(CompanyID=company)

    def perform_update(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        self._validate_relationships(serializer, company)
        serializer.save(CompanyID=company)
