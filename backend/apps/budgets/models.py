from django.db import models
from apps.accounts.models import Company
from apps.accounting.models import ChartOfAccount
from apps.accounts.models import User

class Budget(models.Model):
    BudgetID = models.AutoField(primary_key=True, verbose_name="Budget ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    AccountID = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE, verbose_name="Account")
    Description = models.TextField(null=True, blank=True, verbose_name="Description")
    BudgetYear = models.IntegerField(verbose_name="Budget Year")
    BudgetMonth = models.IntegerField(verbose_name="Budget Month")
    Amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Amount")
    BudgetNotes = models.TextField(null=True, blank=True, verbose_name="Budget Notes")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    UserID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")

    def __str__(self):
        return f"{self.AccountID.AccountName} - {self.BudgetYear}/{self.BudgetMonth:02d}"

    class Meta:
        db_table = 'Budgets'
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
