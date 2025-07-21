from django.db import models
from apps.core.models import Company
from apps.accounts.models import User

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'Employees'

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    gross_pay = models.DecimalField(max_digits=15, decimal_places=2)
    net_pay = models.DecimalField(max_digits=15, decimal_places=2)
    pay_date = models.DateField()

    class Meta:
        db_table = 'Payroll'

class PayrollDeduction(models.Model):
    deduction_id = models.AutoField(primary_key=True)
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deduction_type = models.CharField(max_length=100) # e.g