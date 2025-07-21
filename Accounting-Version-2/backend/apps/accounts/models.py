from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from apps.core.models import Company

class User(AbstractUser):
    companies = models.ManyToManyField(Company, through='UserCompanyRole')
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_set_accounts",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set_accounts",
        related_query_name="user",
    )

    class Meta:
        db_table = 'Users'

class UserCompanyRole(models.Model):
    user_company_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=100) # e.g., 'Admin', 'Accountant', 'Viewer'

    class Meta:
        db_table = 'UserCompanyRole'
        unique_together = ('user', 'company')

class ChartOfAccounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_code = models.CharField(max_length=20)
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50) # e.g., 'Asset', 'Liability', 'Equity', 'Revenue', 'Expense'
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'ChartOfAccounts'
        unique_together = ('company', 'account_code')

class GeneralLedger(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'GeneralLedger'
