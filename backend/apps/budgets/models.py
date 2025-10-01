from django.db import models
from apps.accounts.models import Company
from apps.accounting.models import ChartOfAccount
from apps.accounts.models import User

class Budget(models.Model):
    BudgetID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    AccountID = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    Description = models.TextField(null=True, blank=True)
    BudgetYear = models.IntegerField()
    BudgetMonth = models.IntegerField()
    Amount = models.DecimalField(max_digits=18, decimal_places=2)
    BudgetNotes = models.TextField(null=True, blank=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UserID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.AccountID.AccountName} - {self.BudgetYear}/{self.BudgetMonth:02d}"

    class Meta:
        db_table = 'Budgets'
