from django.db import models
from apps.accounts.models import Company
from apps.projects.models import Project

class Employee(models.Model):
    EmployeeID = models.AutoField(primary_key=True, verbose_name="Employee ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    Name = models.CharField(max_length=200, verbose_name="Name")
    Email = models.EmailField(max_length=255, null=True, blank=True, verbose_name="Email")
    HourlyRate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Hourly Rate")
    TaxWithholding = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Tax Withholding")
    EmployeeNotes = models.TextField(null=True, blank=True, verbose_name="Employee Notes")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'Employees'
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

class Payroll(models.Model):
    PayrollID = models.AutoField(primary_key=True, verbose_name="Payroll ID")
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    PayPeriodStart = models.DateField(verbose_name="Pay Period Start")
    PayPeriodEnd = models.DateField(verbose_name="Pay Period End")
    GrossPay = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Gross Pay")
    NetPay = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Net Pay")
    TaxesWithheld = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Taxes Withheld")
    PaymentDate = models.DateField(verbose_name="Payment Date")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"Payroll for {self.EmployeeID.Name} ({self.PayPeriodStart} - {self.PayPeriodEnd})"

    class Meta:
        db_table = 'Payroll'
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"

class PayrollDeduction(models.Model):
    DeductionID = models.AutoField(primary_key=True, verbose_name="Deduction ID")
    PayrollID = models.ForeignKey(Payroll, on_delete=models.CASCADE, verbose_name="Payroll")
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    DeductionType = models.CharField(max_length=100, verbose_name="Deduction Type")
    Amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Amount")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.DeductionType} - {self.EmployeeID.Name} (${self.Amount})"

    class Meta:
        db_table = 'PayrollDeductions'
        verbose_name = "Payroll Deduction"
        verbose_name_plural = "Payroll Deductions"

class TimeEntry(models.Model):
    TimeEntryID = models.AutoField(primary_key=True, verbose_name="Time Entry ID")
    ProjectID = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='payroll_time_entries', verbose_name="Project")
    EmployeeID = models.ForeignKey('payroll.Employee', on_delete=models.CASCADE, related_name='payroll_time_entries', verbose_name="Employee")
    WorkDate = models.DateField(verbose_name="Work Date")
    Hours = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Hours")
    TimeEntryNotes = models.TextField(null=True, blank=True, verbose_name="Time Entry Notes")
    Billable = models.BooleanField(default=False, verbose_name="Billable")
    Rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Rate")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.EmployeeID.Name} - {self.WorkDate} ({self.Hours}h)"

    class Meta:
        db_table = 'PayrollTimeEntries'
        verbose_name = "Time Entry"
        verbose_name_plural = "Time Entries"

class PayStub(models.Model):
    PayStubID = models.AutoField(primary_key=True, verbose_name="Pay Stub ID")
    PayrollID = models.ForeignKey(Payroll, on_delete=models.CASCADE, verbose_name="Payroll")
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    GrossPay = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Gross Pay")
    NetPay = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Net Pay")
    TotalDeductions = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Total Deductions")
    TotalTaxes = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Total Taxes")
    PayPeriodStart = models.DateField(verbose_name="Pay Period Start")
    PayPeriodEnd = models.DateField(verbose_name="Pay Period End")
    PaymentDate = models.DateField(verbose_name="Payment Date")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"Pay Stub for {self.EmployeeID.Name} - {self.PaymentDate}"

    class Meta:
        db_table = 'PayStubs'
        verbose_name = "Pay Stub"
        verbose_name_plural = "Pay Stubs"

class Tax(models.Model):
    TaxID = models.AutoField(primary_key=True, verbose_name="Tax ID")
    PayrollID = models.ForeignKey(Payroll, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Payroll")
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    TaxType = models.CharField(max_length=100, verbose_name="Tax Type")  # e.g., 'Federal Income', 'Social Security', 'Medicare', 'State Income'
    TaxRate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Tax Rate")  # e.g., 0.0620 for 6.2%
    TaxAmount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Tax Amount")
    TaxYear = models.IntegerField(verbose_name="Tax Year")
    TaxPeriod = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tax Period")  # e.g., 'Q1', 'Monthly'
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.TaxType} - {self.EmployeeID.Name} (${self.TaxAmount})"

    class Meta:
        db_table = 'Taxes'
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"

class Benefit(models.Model):
    BenefitID = models.AutoField(primary_key=True, verbose_name="Benefit ID")
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    BenefitType = models.CharField(max_length=100, verbose_name="Benefit Type")  # e.g., 'Health Insurance', 'Dental', '401k', 'Life Insurance'
    Provider = models.CharField(max_length=200, null=True, blank=True, verbose_name="Provider")
    CoverageAmount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Coverage Amount")
    EmployeeContribution = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Employee Contribution")
    EmployerContribution = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Employer Contribution")
    StartDate = models.DateField(verbose_name="Start Date")
    EndDate = models.DateField(null=True, blank=True, verbose_name="End Date")
    IsActive = models.BooleanField(default=True, verbose_name="Is Active")
    BenefitNotes = models.TextField(null=True, blank=True, verbose_name="Benefit Notes")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.BenefitType} - {self.EmployeeID.Name}"

    class Meta:
        db_table = 'Benefits'
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"
