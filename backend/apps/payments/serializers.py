from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='PaymentID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    invoice_id = serializers.IntegerField(source='InvoiceID', required=False)
    bill_id = serializers.IntegerField(source='BillID', required=False)
    payment_date = serializers.DateField(source='PaymentDate')
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    payment_method = serializers.CharField(source='PaymentMethod', required=False, allow_blank=True)
    notes = serializers.CharField(source='PaymentNotes', required=False, allow_blank=True)
    currency_code = serializers.CharField(source='CurrencyCode', default='USD')
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    user_id = serializers.IntegerField(source='UserID', read_only=True)
    
    class Meta:
        model = Payment
        fields = ('id', 'company_id', 'invoice_id', 'bill_id', 'payment_date', 'amount', 
                 'payment_method', 'notes', 'currency_code', 'created_date', 'user_id')
        read_only_fields = ('id', 'created_date')