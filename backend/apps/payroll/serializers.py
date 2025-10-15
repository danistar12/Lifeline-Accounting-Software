from rest_framework import serializers
from .models import Employee, Payroll, PayrollDeduction, PayStub, Tax, Benefit

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
    # CamelCase aliases for common fields
    EmployeeID = serializers.IntegerField(source='EmployeeID', read_only=True)
    CompanyID = serializers.IntegerField(source='CompanyID', read_only=True)
    Name = serializers.CharField(source='Name', read_only=True)
    Email = serializers.EmailField(source='Email', read_only=True)

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'

class PayrollDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeduction
        fields = '__all__'

class PayStubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayStub
        fields = '__all__'
    # Common aliases used by frontend
    PaystubID = serializers.IntegerField(source='PaystubID', read_only=True)
    PayrollID = serializers.IntegerField(source='PayrollID', read_only=True)
    EmployeeID = serializers.IntegerField(source='EmployeeID', read_only=True)
    EmployeeName = serializers.CharField(source='EmployeeID.Name', read_only=True)
    PayPeriodStart = serializers.DateField(source='PayPeriodStart', read_only=True)
    PayPeriodEnd = serializers.DateField(source='PayPeriodEnd', read_only=True)
    GrossPay = serializers.DecimalField(source='GrossPay', max_digits=18, decimal_places=2, read_only=True)
    NetPay = serializers.DecimalField(source='NetPay', max_digits=18, decimal_places=2, read_only=True)
    Status = serializers.CharField(source='Status', read_only=True)

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'
