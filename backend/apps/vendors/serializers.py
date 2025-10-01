from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='VendorID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    name = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    payment_terms = serializers.CharField(source='PaymentTerms', required=False, allow_blank=True)
    notes = serializers.CharField(source='VendorNotes', required=False, allow_blank=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    
    class Meta:
        model = Vendor
        fields = ('id', 'company_id', 'name', 'email', 'phone', 'address', 'payment_terms', 'notes', 'created_date')
        read_only_fields = ('id', 'created_date')