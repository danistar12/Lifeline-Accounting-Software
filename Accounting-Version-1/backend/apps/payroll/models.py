from django.db import models
from apps.accounts.models import Company
from apps.core.models import Project

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    tax_withholding = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    employee_notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Employees'

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    gross_pay = models.DecimalField(max_digits=18, decimal_places=2)
    net_pay = models.DecimalField(max_digits=18, decimal_places=2)
    taxes_withheld = models.DecimalField(max_digits=18, decimal_places=2)
    payment_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Payroll'

class PayrollDeduction(models.Model):
    deduction_id = models.AutoField(primary_key=True)
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deduction_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PayrollDeductions'

class TimeEntry(models.Model):
    time_entry_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_time_entries')
    work_date = models.DateField()
    hours = models.DecimalField(max_digits=18, decimal_places=2)
    time_entry_notes = models.TextField(null=True, blank=True)
    billable = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PayrollTimeEntries'
