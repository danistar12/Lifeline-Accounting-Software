from rest_framework import serializers
from .models import User, UserCompanyRole, ChartOfAccounts, GeneralLedger

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'companies']

class UserCompanyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompanyRole
        fields = '__all__'

class ChartOfAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartOfAccounts
        fields = '__all__'

class GeneralLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralLedger
        fields = '__all__'
