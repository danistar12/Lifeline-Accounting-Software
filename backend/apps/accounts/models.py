from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    UserNotes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Users'

class Company(models.Model):
    CompanyID = models.AutoField(primary_key=True)
    CompanyName = models.CharField(max_length=100)
    CompanyNotes = models.TextField(null=True, blank=True)
    AdminUserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='administered_companies')
    CreatedDate = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, through='UserCompanyRole', related_name='companies')

    def __str__(self):
        return self.CompanyName

    class Meta:
        db_table = 'Companies'

class UserCompanyRole(models.Model):
    UserCompanyRoleID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    Role = models.CharField(max_length=50)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.UserID.username} - {self.CompanyID.CompanyName}'

    class Meta:
        db_table = 'UserCompanyRole'
        unique_together = (('UserID', 'CompanyID'),)
