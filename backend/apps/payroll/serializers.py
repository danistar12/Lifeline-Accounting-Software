from rest_framework import serializers
from .models import Employee, Payroll, PayrollDeduction, PayStub, Tax, Benefit

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
    # CamelCase aliases for common fields
    EmployeeID = serializers.IntegerField(read_only=True)
    # Return the FK integer id instead of the related Company object
    CompanyID = serializers.IntegerField(source='CompanyID_id', read_only=True)
    Name = serializers.CharField(read_only=True)
    Email = serializers.EmailField(read_only=True)

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
    PaystubID = serializers.IntegerField(read_only=True)
    PayrollID = serializers.IntegerField(read_only=True)
    EmployeeID = serializers.IntegerField(read_only=True)
    EmployeeName = serializers.CharField(source='EmployeeID.Name', read_only=True)
    PayPeriodStart = serializers.DateField(read_only=True)
    PayPeriodEnd = serializers.DateField(read_only=True)
    GrossPay = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    NetPay = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    Status = serializers.CharField(read_only=True)

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'
