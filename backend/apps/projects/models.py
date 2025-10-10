from django.db import models
from apps.accounts.models import Company
from apps.customers.models import Customer

class Project(models.Model):
    ProjectID = models.AutoField(primary_key=True, verbose_name="Project ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    ProjectName = models.CharField(max_length=200, verbose_name="Project Name")
    CustomerID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Customer")
    StartDate = models.DateField(null=True, blank=True, verbose_name="Start Date")
    EndDate = models.DateField(null=True, blank=True, verbose_name="End Date")
    Budget = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Budget")
    ProjectNotes = models.TextField(null=True, blank=True, verbose_name="Project Notes")
    Status = models.CharField(max_length=50, verbose_name="Status")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return self.ProjectName

    class Meta:
        db_table = 'Projects'
        verbose_name = "Project"
        verbose_name_plural = "Projects"

