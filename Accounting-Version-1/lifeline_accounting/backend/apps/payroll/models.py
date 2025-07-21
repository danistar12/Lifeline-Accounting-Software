from django.db import models
from apps.accounts.models import Company
from apps.core.models import Customer

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Employees'

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    run_date = models.DateField()
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()

    class Meta:
        db_table = 'Payroll'

class Paystub(models.Model):
    paystub_id = models.AutoField(primary_key=True)
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    gross_pay = models.DecimalField(max_digits=18, decimal_places=2)
    net_pay = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'Paystubs'

class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    paystub = models.ForeignKey(Paystub, on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=100)
    tax_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'Taxes'

class Deduction(models.Model):
    deduction_id = models.AutoField(primary_key=True)
    paystub = models.ForeignKey(Paystub, on_delete=models.CASCADE)
    deduction_name = models.CharField(max_length=100)
    deduction_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'Deductions'

class Benefit(models.Model):
    benefit_id = models.AutoField(primary_key=True)
    paystub = models.ForeignKey(Paystub, on_delete=models.CASCADE)
    benefit_name = models.CharField(max_length=100)
    benefit_amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'Benefits'
