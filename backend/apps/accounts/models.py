from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    UserNotes = models.TextField(null=True, blank=True, verbose_name="User Notes")

    class Meta:
        db_table = 'Users'
        verbose_name = "User"
        verbose_name_plural = "Users"

class Company(models.Model):
    CompanyID = models.AutoField(primary_key=True, verbose_name="Company ID")
    CompanyName = models.CharField(max_length=100, verbose_name="Company Name")
    CompanyNotes = models.TextField(null=True, blank=True, verbose_name="Company Notes")
    AdminUserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='administered_companies', verbose_name="Admin User")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    users = models.ManyToManyField(User, through='UserCompanyRole', related_name='companies')

    def __str__(self):
        return self.CompanyName

    class Meta:
        db_table = 'Companies'
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class UserCompanyRole(models.Model):
    UserCompanyRoleID = models.AutoField(primary_key=True, verbose_name="User Company Role ID")
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    Role = models.CharField(max_length=50, verbose_name="Role")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f'{self.UserID.username} - {self.CompanyID.CompanyName}'

    class Meta:
        db_table = 'UserCompanyRole'
        verbose_name = "User Company Role"
        verbose_name_plural = "User Company Roles"
        unique_together = (('UserID', 'CompanyID'),)


class UserSettings(models.Model):
    """User preferences and application settings"""
    UserID = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        verbose_name="User",
        related_name='settings'
    )
    
    # Notification Preferences
    EmailNotifications = models.BooleanField(
        default=True, 
        verbose_name="Email Notifications"
    )
    DesktopNotifications = models.BooleanField(
        default=False, 
        verbose_name="Desktop Notifications"
    )
    NotificationTypes = models.JSONField(
        default=dict,
        verbose_name="Notification Types",
        help_text="Which types of notifications to receive"
    )
    
    # Application Preferences
    AutoSaveForms = models.BooleanField(
        default=True, 
        verbose_name="Auto-save Forms"
    )
    DefaultCompany = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Default Company",
        related_name='default_for_users'
    )
    DateFormat = models.CharField(
        max_length=20,
        default='MM/DD/YYYY',
        verbose_name="Date Format"
    )
    CurrencyFormat = models.CharField(
        max_length=10,
        default='USD',
        verbose_name="Currency Format"
    )
    Theme = models.CharField(
        max_length=20,
        choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')],
        default='light',
        verbose_name="Theme"
    )
    
    # Privacy & Security
    TwoFactorEnabled = models.BooleanField(
        default=False,
        verbose_name="Two-Factor Authentication"
    )
    SessionTimeout = models.IntegerField(
        default=30,
        verbose_name="Session Timeout (minutes)"
    )
    
    # Data Export Preferences
    LastExportDate = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Last Export Date"
    )
    
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name="Modified Date")

    def __str__(self):
        return f"Settings for {self.UserID.username}"

    class Meta:
        db_table = 'UserSettings'
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"
