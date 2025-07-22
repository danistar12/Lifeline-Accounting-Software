from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from apps.core.models import Company

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, db_column='UserID')
    username = models.CharField(max_length=150, unique=True, db_column='Username')
    password_hash = models.CharField(max_length=128, db_column='PasswordHash')
    email = models.EmailField(db_column='Email')
    user_notes = models.TextField(blank=True, null=True, db_column='UserNotes')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    
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

    # Override the password field to use our custom field
    def save(self, *args, **kwargs):
        if self.password and not self.password_hash:
            self.password_hash = self.password
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Users'

class UserCompanyRole(models.Model):
    user_company_role_id = models.AutoField(primary_key=True, db_column='UserCompanyRoleID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    role = models.CharField(max_length=100, db_column='Role')  # e.g., 'Admin', 'Accountant', 'Viewer'
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    class Meta:
        db_table = 'UserCompanyRole'
        unique_together = ('user', 'company')

class AuditLog(models.Model):
    audit_id = models.AutoField(primary_key=True, db_column='AuditID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='UserID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    action = models.CharField(max_length=100, db_column='Action')
    table_name = models.CharField(max_length=100, db_column='TableName')
    record_id = models.IntegerField(db_column='RecordID')
    action_date = models.DateTimeField(auto_now_add=True, db_column='ActionDate')
    details = models.TextField(blank=True, null=True, db_column='Details')

    def __str__(self):
        return f"{self.action} on {self.table_name} by {self.user}"

    class Meta:
        db_table = 'AuditLog'
