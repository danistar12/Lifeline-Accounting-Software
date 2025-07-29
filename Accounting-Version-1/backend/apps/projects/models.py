from django.db import models
from apps.core.models import Company, Customer

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    project_notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Projects'

class TimeEntry(models.Model):
    time_entry_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey('payroll.Employee', on_delete=models.CASCADE, related_name='project_time_entries')
    work_date = models.DateField()
    hours = models.DecimalField(max_digits=18, decimal_places=2)
    time_entry_notes = models.TextField(null=True, blank=True)
    billable = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ProjectTimeEntries'
