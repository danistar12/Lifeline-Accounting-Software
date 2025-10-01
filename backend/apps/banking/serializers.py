from rest_framework import serializers
from .models import BankAccount, BankStatementLine, ReconciliationEntry

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class BankStatementLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStatementLine
        fields = '__all__'

class ReconciliationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationEntry
        fields = '__all__'
