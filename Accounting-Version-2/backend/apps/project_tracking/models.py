from django.db import models
from apps.core.models import Company
from apps.contacts.models import Customer
from apps.payroll.models import Employee

class Project(models.Model):
    project_id = models.AutoField(primary_key=True, db_column='ProjectID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    project_name = models.CharField(max_length=255, db_column='ProjectName')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, db_column='CustomerID')
    start_date = models.DateField(db_column='StartDate', null=True, blank=True)
    end_date = models.DateField(db_column='EndDate', null=True, blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, db_column='Budget')
    project_notes = models.TextField(blank=True, null=True, db_column='ProjectNotes')
    status = models.CharField(max_length=50, db_column='Status')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'Projects'

class TimeEntry(models.Model):
    time_entry_id = models.AutoField(primary_key=True, db_column='TimeEntryID')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='ProjectID')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='EmployeeID')
    work_date = models.DateField(db_column='WorkDate')
    hours = models.DecimalField(max_digits=5, decimal_places=2, db_column='Hours')
    time_entry_notes = models.TextField(blank=True, null=True, db_column='TimeEntryNotes')
    billable = models.BooleanField(default=True, db_column='Billable')
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='Rate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.employee} - {self.project} - {self.work_date}"

    class Meta:
        db_table = 'TimeEntries'
        verbose_name_plural = "Time Entries"
