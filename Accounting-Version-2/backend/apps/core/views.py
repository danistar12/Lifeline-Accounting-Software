from django.shortcuts import render
from rest_framework import viewsets

from .models import Company, ChartOfAccounts, GeneralLedger
from .serializers import CompanySerializer, ChartOfAccountsSerializer, GeneralLedgerSerializer
from apps.core.permissions import HasCompanyRole

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['GlobalAdmin']  # Only Global Admins can manage companies

    def get_queryset(self):
        # Global admins can see all companies
        if self.request.user.is_staff:  # A simple way to distinguish global admins
            return Company.objects.all()
        # Other users can only see companies they are associated with
        return self.request.user.companies.all()

class ChartOfAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = ChartOfAccountsSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Manager', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return ChartOfAccounts.objects.filter(company_id=company_id)
        return ChartOfAccounts.objects.none()

class GeneralLedgerViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralLedgerSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Manager', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return GeneralLedger.objects.filter(company_id=company_id)
        return GeneralLedger.objects.none()
