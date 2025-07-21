from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    user_notes = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    class Meta:
        db_table = 'Users'

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    company_notes = models.TextField(null=True, blank=True)
    
    # Contact Information
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    
    # Address Information
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True, default='United States')
    
    # Business Information
    website = models.URLField(null=True, blank=True)
    tax_id = models.CharField(max_length=50, null=True, blank=True, help_text="Tax ID/EIN")
    
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='administered_companies')
    created_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, through='UserCompanyRole', related_name='companies')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'Companies'

class UserCompanyRole(models.Model):
    user_company_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.company.company_name}'

    class Meta:
        db_table = 'UserCompanyRole'
        unique_together = (('user', 'company'),)
