from django.db import models
from apps.accounts.models import Company
from apps.projects.models import Project

class Employee(models.Model):
    EmployeeID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=255, null=True, blank=True)
    HourlyRate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    TaxWithholding = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    EmployeeNotes = models.TextField(null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'Employees'

class Payroll(models.Model):
    PayrollID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    PayPeriodStart = models.DateField()
    PayPeriodEnd = models.DateField()
    GrossPay = models.DecimalField(max_digits=18, decimal_places=2)
    NetPay = models.DecimalField(max_digits=18, decimal_places=2)
    TaxesWithheld = models.DecimalField(max_digits=18, decimal_places=2)
    PaymentDate = models.DateField()
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payroll for {self.EmployeeID.Name} ({self.PayPeriodStart} - {self.PayPeriodEnd})"

    class Meta:
        db_table = 'Payroll'

class PayrollDeduction(models.Model):
    DeductionID = models.AutoField(primary_key=True)
    PayrollID = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    DeductionType = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=18, decimal_places=2)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.DeductionType} - {self.EmployeeID.Name} (${self.Amount})"

    class Meta:
        db_table = 'PayrollDeductions'

class TimeEntry(models.Model):
    TimeEntryID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='payroll_time_entries')
    EmployeeID = models.ForeignKey('payroll.Employee', on_delete=models.CASCADE, related_name='payroll_time_entries')
    WorkDate = models.DateField()
    Hours = models.DecimalField(max_digits=18, decimal_places=2)
    TimeEntryNotes = models.TextField(null=True, blank=True)
    Billable = models.BooleanField(default=False)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.EmployeeID.Name} - {self.WorkDate} ({self.Hours}h)"

    class Meta:
        db_table = 'PayrollTimeEntries'
