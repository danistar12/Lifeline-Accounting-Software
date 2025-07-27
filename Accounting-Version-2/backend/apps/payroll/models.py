from django.db import models
from apps.core.models import Company
from apps.accounts.models import User

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, db_column='EmployeeID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    name = models.CharField(max_length=255, db_column='Name')
    email = models.EmailField(db_column='Email')
    hourly_rate = models.DecimalField(max_digits=15, decimal_places=2, db_column='HourlyRate')
    tax_withholding = models.DecimalField(max_digits=15, decimal_places=2, db_column='TaxWithholding')
    employee_notes = models.TextField(blank=True, null=True, db_column='EmployeeNotes')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    class Meta:
        db_table = 'Employees'
        
    def __str__(self):
        return f"{self.name} ({self.email})"

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True, db_column='PayrollID')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='EmployeeID')
    pay_period_start = models.DateField(db_column='PayPeriodStart')
    pay_period_end = models.DateField(db_column='PayPeriodEnd')
    gross_pay = models.DecimalField(max_digits=15, decimal_places=2, db_column='GrossPay')
    net_pay = models.DecimalField(max_digits=15, decimal_places=2, db_column='NetPay')
    taxes_withheld = models.DecimalField(max_digits=15, decimal_places=2, db_column='TaxesWithheld')
    payment_date = models.DateField(db_column='PaymentDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    class Meta:
        db_table = 'Payroll'
        
    def __str__(self):
        return f"Payroll for {self.employee.name} ({self.pay_period_start} to {self.pay_period_end})"

class PayrollDeduction(models.Model):
    deduction_id = models.AutoField(primary_key=True, db_column='DeductionID')
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, db_column='PayrollID')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='EmployeeID')
    deduction_type = models.CharField(max_length=100, db_column='DeductionType')
    amount = models.DecimalField(max_digits=15, decimal_places=2, db_column='Amount')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    class Meta:
        db_table = 'PayrollDeductions'
        
    def __str__(self):
        return f"{self.deduction_type} deduction for {self.employee.name} - ${self.amount}"