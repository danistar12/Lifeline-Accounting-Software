from rest_framework import serializers
from .models import User, Company, UserCompanyRole

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
