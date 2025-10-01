from django.db import models
from apps.accounts.models import Company
from apps.customers.models import Customer

class Subscription(models.Model):
    SubscriptionID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    PlanName = models.CharField(max_length=100)
    BillingCycle = models.CharField(max_length=50)
    RenewalDate = models.DateField()
    Status = models.CharField(max_length=20, default='Active')
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.CustomerID.Name} - {self.PlanName}"

    class Meta:
        db_table = 'Subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
