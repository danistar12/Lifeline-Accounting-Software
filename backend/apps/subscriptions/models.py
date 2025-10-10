from django.db import models
from apps.accounts.models import Company
from apps.customers.models import Customer

class Subscription(models.Model):
    SubscriptionID = models.AutoField(primary_key=True, verbose_name="Subscription ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    PlanName = models.CharField(max_length=100, verbose_name="Plan Name")
    BillingCycle = models.CharField(max_length=50, verbose_name="Billing Cycle")
    RenewalDate = models.DateField(verbose_name="Renewal Date")
    Status = models.CharField(max_length=20, default='Active', verbose_name="Status")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.CustomerID.Name} - {self.PlanName}"

    class Meta:
        db_table = 'Subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
