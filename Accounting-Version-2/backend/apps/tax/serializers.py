from rest_framework import serializers
from .models import TaxRate, TaxTransaction

class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = '__all__'

class TaxTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxTransaction
        fields = '__all__'
