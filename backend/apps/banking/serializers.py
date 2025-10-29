from rest_framework import serializers
from .models import BankAccount, BankStatementLine, ReconciliationEntry

class BankAccountSerializer(serializers.ModelSerializer):
    # Map frontend field names to backend model fields
    id = serializers.IntegerField(source='BankAccountID', read_only=True)
    name = serializers.CharField(source='BankName')
    account_number = serializers.CharField(source='AccountNumber')
    bank_name = serializers.CharField(source='BankName')
    type = serializers.CharField(source='AccountType', required=False, allow_blank=True)
    balance = serializers.DecimalField(source='Balance', max_digits=18, decimal_places=2)
    
    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'account_number', 'bank_name', 'type', 'balance']

class BankStatementLineSerializer(serializers.ModelSerializer):
    # Map frontend field names to backend model fields
    id = serializers.IntegerField(source='BankStatementLineID', read_only=True)
    date = serializers.DateTimeField(source='TransactionDate')
    description = serializers.CharField(source='Description')
    amount = serializers.DecimalField(source='Amount', max_digits=18, decimal_places=2)
    reference_number = serializers.CharField(source='TransactionNumber', allow_blank=True, allow_null=True)
    memo = serializers.CharField(source='BankAcctNotes', allow_blank=True, allow_null=True, required=False)
    status = serializers.CharField(source='MatchStatus', allow_blank=True, allow_null=True, required=False)
    
    class Meta:
        model = BankStatementLine
        fields = ['id', 'date', 'description', 'amount', 'reference_number', 'memo', 'status']

class ReconciliationEntrySerializer(serializers.ModelSerializer):
    # Map frontend field names to backend model fields
    id = serializers.IntegerField(source='ReconciliationEntryID', read_only=True)
    reconciled_date = serializers.DateTimeField(source='ReconciledDate')
    amount = serializers.DecimalField(source='ReconciledAmount', max_digits=18, decimal_places=2)
    account_name = serializers.SerializerMethodField()
    statement_line_ref = serializers.SerializerMethodField()
    statement_description = serializers.SerializerMethodField()
    gl_transaction_ref = serializers.SerializerMethodField()
    gl_description = serializers.SerializerMethodField()
    
    def get_account_name(self, obj):
        try:
            return obj.BankStatementLineID.BankAccountID.BankName if obj.BankStatementLineID and obj.BankStatementLineID.BankAccountID else None
        except AttributeError:
            return None
    
    def get_statement_line_ref(self, obj):
        try:
            return obj.BankStatementLineID.TransactionNumber if obj.BankStatementLineID else None
        except AttributeError:
            return None
    
    def get_statement_description(self, obj):
        try:
            return obj.BankStatementLineID.Description if obj.BankStatementLineID else None
        except AttributeError:
            return None
    
    def get_gl_transaction_ref(self, obj):
        try:
            return str(obj.GeneralLedgerID.GeneralLedgerID) if obj.GeneralLedgerID else None
        except AttributeError:
            return None
    
    def get_gl_description(self, obj):
        try:
            return obj.GeneralLedgerID.Description if obj.GeneralLedgerID else None
        except AttributeError:
            return None
    
    class Meta:
        model = ReconciliationEntry
        fields = ['id', 'reconciled_date', 'amount', 'account_name', 'statement_line_ref', 
                 'statement_description', 'gl_transaction_ref', 'gl_description']
