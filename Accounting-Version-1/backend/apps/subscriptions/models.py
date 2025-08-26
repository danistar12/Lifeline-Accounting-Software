from django.db import models
from apps.core.models import Company, Customer

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    billing_cycle = models.CharField(max_length=50)
    renewal_date = models.DateField()
    status = models.CharField(max_length=20, default='Active')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.plan_name}"

    class Meta:
        db_table = 'Subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
