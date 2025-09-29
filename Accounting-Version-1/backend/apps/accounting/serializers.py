from rest_framework import serializers
from .models import ChartOfAccount, GeneralLedger

class ChartOfAccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='AccountID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    code = serializers.CharField(source='AccountCode')
    name = serializers.CharField(source='AccountName')
    type = serializers.CharField(source='AccountType')
    notes = serializers.CharField(source='AccountNotes', required=False, allow_blank=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    is_active = serializers.BooleanField(source='IsActive', default=True)
    
    class Meta:
        model = ChartOfAccount
        fields = ('id', 'company_id', 'code', 'name', 'type', 'notes', 'created_date', 'is_active')
        read_only_fields = ('id', 'created_date')

class GeneralLedgerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='TransactionID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    account_id = serializers.IntegerField(source='AccountID', read_only=True)
    account = ChartOfAccountSerializer(source='AccountID', read_only=True)
    transaction_date = serializers.DateTimeField(source='TransactionDate')
    description = serializers.CharField(required=False, allow_blank=True)
    debit_amount = serializers.DecimalField(source='DebitAmount', max_digits=18, decimal_places=2)
    credit_amount = serializers.DecimalField(source='CreditAmount', max_digits=18, decimal_places=2)
    notes = serializers.CharField(source='GLNotes', required=False, allow_blank=True)
    currency_code = serializers.CharField(source='CurrencyCode', default='USD')
    exchange_rate = serializers.DecimalField(source='ExchangeRate', max_digits=10, decimal_places=6, default=1.000000)
    user_id = serializers.IntegerField(source='UserID', read_only=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    
    class Meta:
        model = GeneralLedger
        fields = ('id', 'company_id', 'account_id', 'account', 'transaction_date', 'description', 
                 'debit_amount', 'credit_amount', 'notes', 'currency_code', 'exchange_rate', 
                 'user_id', 'created_date')
        read_only_fields = ('id', 'created_date')