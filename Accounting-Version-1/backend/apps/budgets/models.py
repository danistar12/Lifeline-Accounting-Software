from django.db import models
from apps.core.models import Company, ChartOfAccount
from apps.accounts.models import User

class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    budget_year = models.IntegerField()
    budget_month = models.IntegerField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    budget_notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Budgets'
