from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    # existing snake_case fields (keep for backward compatibility)
    id = serializers.IntegerField(source='CustomerID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    name = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    payment_terms = serializers.CharField(source='PaymentTerms', required=False, allow_blank=True)
    notes = serializers.CharField(source='CustomerNotes', required=False, allow_blank=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)

    # CamelCase aliases emitted for transition to canonical DB names
    CustomerID = serializers.IntegerField(source='CustomerID', read_only=True)
    CompanyID = serializers.IntegerField(source='CompanyID', read_only=True)
    Name = serializers.CharField(source='Name', read_only=True)
    PaymentTerms = serializers.CharField(source='PaymentTerms', read_only=True)
    CustomerNotes = serializers.CharField(source='CustomerNotes', read_only=True)
    CreatedDate = serializers.DateTimeField(source='CreatedDate', read_only=True)
    
    class Meta:
        model = Customer
        fields = ('id', 'company_id', 'name', 'email', 'phone', 'address', 'payment_terms', 'notes', 'created_date')
        read_only_fields = ('id', 'created_date')