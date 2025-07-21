from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    admin_user = models.ForeignKey('accounts.User', related_name='admin_of_companies', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Companies'
        verbose_name_plural = "Companies"
