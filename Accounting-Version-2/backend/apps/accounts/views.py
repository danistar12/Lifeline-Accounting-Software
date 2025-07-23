from django.shortcuts import render
from rest_framework import viewsets
from .models import User, UserCompanyRole
from apps.core.models import ChartOfAccounts, GeneralLedger
from .serializers import UserSerializer, UserCompanyRoleSerializer, ChartOfAccountsSerializer, GeneralLedgerSerializer
from apps.core.permissions import HasCompanyRole

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin'] # Company Admins can manage users

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return User.objects.filter(companies__company_id=company_id)

class UserCompanyRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserCompanyRoleSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin'] # Company Admins can manage roles

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return UserCompanyRole.objects.filter(company_id=company_id)

class ChartOfAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = ChartOfAccountsSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return ChartOfAccounts.objects.filter(company_id=company_id)

class GeneralLedgerViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralLedgerSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Customer'] # Customer might have read-only access

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return GeneralLedger.objects.filter(company_id=company_id)
