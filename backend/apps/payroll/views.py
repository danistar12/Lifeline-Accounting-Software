from rest_framework import viewsets
from .models import Employee, Payroll, PayrollDeduction, PayStub, Tax, Benefit
from .serializers import EmployeeSerializer, PayrollSerializer, PayrollDeductionSerializer, PayStubSerializer, TaxSerializer, BenefitSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

class PayrollDeductionViewSet(viewsets.ModelViewSet):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer

class PayStubViewSet(viewsets.ModelViewSet):
    queryset = PayStub.objects.all()
    serializer_class = PayStubSerializer

class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
