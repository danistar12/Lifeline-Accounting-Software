from rest_framework import viewsets
from .models import Employee, Payroll, Paystub, Tax, Deduction, Benefit
from .serializers import EmployeeSerializer, PayrollSerializer, PaystubSerializer, TaxSerializer, DeductionSerializer, BenefitSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

class PaystubViewSet(viewsets.ModelViewSet):
    queryset = Paystub.objects.all()
    serializer_class = PaystubSerializer

class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer

class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
