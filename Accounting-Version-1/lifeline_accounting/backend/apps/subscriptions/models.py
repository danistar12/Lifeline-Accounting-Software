from django.db import models
from apps.accounts.models import Company, User

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    billing_cycle = models.CharField(max_length=50)
    renewal_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Active')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Subscriptions'
