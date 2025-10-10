from rest_framework import serializers
from .models import User, Company, UserCompanyRole, UserSettings

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='CompanyID', read_only=True)
    name = serializers.CharField(source='CompanyName')
    notes = serializers.CharField(source='CompanyNotes', required=False, allow_blank=True)
    admin_user_id = serializers.IntegerField(source='AdminUserID_id', required=False, allow_null=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    
    class Meta:
        model = Company
        fields = ('id', 'name', 'notes', 'admin_user_id', 'created_date')
        read_only_fields = ('id', 'created_date')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class UserCompanyRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='UserCompanyRoleID', read_only=True)
    user_id = serializers.IntegerField(source='UserID_id', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID_id', read_only=True)
    role = serializers.CharField(source='Role')
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    company = CompanySerializer(source='CompanyID', read_only=True)
    
    class Meta:
        model = UserCompanyRole
        fields = ('id', 'user_id', 'company_id', 'role', 'created_date', 'company')
        read_only_fields = ('id', 'created_date')


class UserSettingsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='UserID_id', read_only=True)
    email_notifications = serializers.BooleanField(source='EmailNotifications', required=False)
    desktop_notifications = serializers.BooleanField(source='DesktopNotifications', required=False)
    notification_types = serializers.JSONField(source='NotificationTypes', required=False)
    auto_save_forms = serializers.BooleanField(source='AutoSaveForms', required=False)
    default_company = serializers.PrimaryKeyRelatedField(
        source='DefaultCompany',
        queryset=Company.objects.all(),
        required=False,
        allow_null=True
    )
    default_company_details = CompanySerializer(source='DefaultCompany', read_only=True)
    date_format = serializers.CharField(source='DateFormat', required=False)
    currency_format = serializers.CharField(source='CurrencyFormat', required=False)
    theme = serializers.CharField(source='Theme', required=False)
    two_factor_enabled = serializers.BooleanField(source='TwoFactorEnabled', required=False)
    session_timeout = serializers.IntegerField(source='SessionTimeout', required=False)
    last_export_date = serializers.DateTimeField(source='LastExportDate', read_only=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    modified_date = serializers.DateTimeField(source='ModifiedDate', read_only=True)
    
    class Meta:
        model = UserSettings
        fields = (
            'user_id', 'email_notifications', 'desktop_notifications', 'notification_types',
            'auto_save_forms', 'default_company', 'default_company_details', 'date_format',
            'currency_format', 'theme', 'two_factor_enabled', 'session_timeout',
            'last_export_date', 'created_date', 'modified_date'
        )
        read_only_fields = ('user_id', 'last_export_date', 'created_date', 'modified_date')
