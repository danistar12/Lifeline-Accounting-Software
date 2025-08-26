from rest_framework import serializers
from .models import User, Company, UserCompanyRole

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'company_id', 'company_name', 'company_notes', 
            'admin_user', 'created_date'
        )
        read_only_fields = ('company_id', 'created_date')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'user_notes', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class UserCompanyRoleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = UserCompanyRole
        fields = ('user_company_role_id', 'user', 'company', 'role', 'created_date')
        read_only_fields = ('user_company_role_id', 'created_date')
