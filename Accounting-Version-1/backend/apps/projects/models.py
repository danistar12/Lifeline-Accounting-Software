from django.db import models
from apps.accounts.models import Company
from apps.customers.models import Customer

class Project(models.Model):
    ProjectID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    ProjectName = models.CharField(max_length=200)
    CustomerID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    StartDate = models.DateField(null=True, blank=True)
    EndDate = models.DateField(null=True, blank=True)
    Budget = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ProjectNotes = models.TextField(null=True, blank=True)
    Status = models.CharField(max_length=50)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ProjectName

    class Meta:
        db_table = 'Projects'

