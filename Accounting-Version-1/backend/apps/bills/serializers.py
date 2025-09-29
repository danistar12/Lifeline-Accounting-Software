from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='BillID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    vendor_id = serializers.IntegerField(source='VendorID', read_only=True)
    vendor = serializers.SerializerMethodField()
    bill_number = serializers.CharField(source='BillNumber')
    bill_date = serializers.DateField(source='BillDate')
    due_date = serializers.DateField(source='DueDate')
    total_amount = serializers.DecimalField(source='TotalAmount', max_digits=18, decimal_places=2)
    status = serializers.CharField()
    notes = serializers.CharField(source='BillNotes', required=False, allow_blank=True)
    currency_code = serializers.CharField(source='CurrencyCode', default='USD')
    user_id = serializers.IntegerField(source='UserID', read_only=True)
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    modified_date = serializers.DateTimeField(source='ModifiedDate', read_only=True)
    
    def get_vendor(self, obj):
        return {
            'id': obj.VendorID.VendorID,
            'name': obj.VendorID.Name,
            'email': obj.VendorID.Email
        }
    
    class Meta:
        model = Bill
        fields = ('id', 'company_id', 'vendor_id', 'vendor', 'bill_number', 'bill_date', 'due_date', 
                 'total_amount', 'status', 'notes', 'currency_code', 'user_id', 'created_date', 'modified_date')
        read_only_fields = ('id', 'created_date', 'modified_date')