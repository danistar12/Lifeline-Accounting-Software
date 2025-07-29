from rest_framework import viewsets
from .models import Employee, Payroll, PayrollDeduction
from .serializers import EmployeeSerializer, PayrollSerializer, PayrollDeductionSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

class PayrollDeductionViewSet(viewsets.ModelViewSet):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer
