from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, UserCompanyRole
from apps.core.models import ChartOfAccounts, GeneralLedger

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True}
        }
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    companies = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name', 
            'phone', 'avatar', 'avatar_url', 'full_name', 'user_notes', 
            'created_date', 'last_login_date', 'companies'
        ]
        read_only_fields = ['user_id', 'username', 'created_date', 'last_login_date']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_companies(self, obj):
        companies = []
        for role in obj.usercompanyrole_set.all():
            companies.append({
                'company_id': role.company.company_id,
                'name': role.company.company_name,  # Fixed: use company_name instead of name
                'role': role.role
            })
        return companies

class UserCompanyRoleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    company_name = serializers.CharField(source='company.company_name', read_only=True)  # Fixed: use company_name field
    
    class Meta:
        model = UserCompanyRole
        fields = ['user_company_role_id', 'user', 'company', 'role', 'created_date', 'user_name', 'company_name']

class ChartOfAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartOfAccounts
        fields = '__all__'

class GeneralLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralLedger
        fields = '__all__'
