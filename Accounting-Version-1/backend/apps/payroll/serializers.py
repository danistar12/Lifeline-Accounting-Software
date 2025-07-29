from rest_framework import serializers
from .models import Employee, Payroll, PayrollDeduction

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'

class PayrollDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeduction
        fields = '__all__'
