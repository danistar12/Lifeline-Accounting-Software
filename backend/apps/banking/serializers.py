from rest_framework import serializers
from .models import BankAccount, BankStatementLine, ReconciliationEntry


class BankAccountSerializer(serializers.ModelSerializer):
    # Map frontend field names to backend model fields
    id = serializers.IntegerField(source='BankAccountID', read_only=True)
    name = serializers.SerializerMethodField()
    account_number = serializers.CharField(source='AccountNumber', allow_blank=True, required=False)
    bank_name = serializers.CharField(source='BankName', allow_blank=True, required=False)
    type = serializers.CharField(source='AccountType', required=False, allow_blank=True)
    balance = serializers.SerializerMethodField()

    def get_name(self, obj):
        if getattr(obj, 'BankName', None):
            return obj.BankName
        if getattr(obj, 'AccountType', None):
            return obj.AccountType
        if getattr(obj, 'AccountNumber', None):
            return f"Account {obj.AccountNumber}"
        return ''

    def get_balance(self, obj):
        if obj.Balance is None:
            return None
        try:
            return float(obj.Balance)
        except (TypeError, ValueError):
            return None

    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'account_number', 'bank_name', 'type', 'balance']


class BankStatementLineSerializer(serializers.ModelSerializer):
    # Map frontend field names to backend model fields
    id = serializers.IntegerField(source='BankStatementLineID', read_only=True)
    date = serializers.DateTimeField(source='TransactionDate')
    description = serializers.CharField(source='Description')
    amount = serializers.SerializerMethodField()
    reference_number = serializers.CharField(source='TransactionNumber', allow_blank=True, allow_null=True)
    memo = serializers.CharField(source='BankAcctNotes', allow_blank=True, allow_null=True, required=False)
    status = serializers.SerializerMethodField()
    is_imported = serializers.BooleanField(source='IsImported', read_only=True)

    def get_amount(self, obj):
        if obj.Amount is None:
            return None
        try:
            return float(obj.Amount)
        except (TypeError, ValueError):
            return None

    def get_status(self, obj):
        raw = getattr(obj, 'MatchStatus', None)
        if raw is None:
            return None
        normalized = str(raw).strip().lower()
        if normalized in ('', 'false', '0', 'no', 'none', 'null'):
            return None
        if normalized in ('true', '1', 'yes'):
            return 'Matched'
        return str(raw)

    class Meta:
        model = BankStatementLine
        fields = ['id', 'date', 'description', 'amount', 'reference_number', 'memo', 'status', 'is_imported']


class ReconciliationEntrySerializer(serializers.ModelSerializer):
    # Map frontend field names to backend model fields
    id = serializers.IntegerField(source='ReconciliationEntryID', read_only=True)
    reconciled_date = serializers.DateTimeField(source='ReconciledDate')
    amount = serializers.SerializerMethodField()
    account_name = serializers.SerializerMethodField()
    statement_line_ref = serializers.SerializerMethodField()
    statement_description = serializers.SerializerMethodField()
    gl_transaction_ref = serializers.SerializerMethodField()
    gl_description = serializers.SerializerMethodField()

    def get_amount(self, obj):
        if obj.ReconciledAmount is None:
            return None
        try:
            return float(obj.ReconciledAmount)
        except (TypeError, ValueError):
            return None
    
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
