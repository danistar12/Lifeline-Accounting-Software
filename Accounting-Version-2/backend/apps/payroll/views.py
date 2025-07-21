from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee, Payroll, PayrollDeduction
from .serializers import EmployeeSerializer, PayrollSerializer, PayrollDeductionSerializer
from apps.core.permissions import HasCompanyRole

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Employee.objects.filter(company_id=company_id)

class PayrollViewSet(viewsets.ModelViewSet):
    serializer_class = PayrollSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Payroll.objects.filter(employee__company_id=company_id)

class PayrollDeductionViewSet(viewsets.ModelViewSet):
    serializer_class = PayrollDeductionSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return PayrollDeduction.objects.filter(employee__company_id=company_id)
