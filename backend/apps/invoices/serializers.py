from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    CustomerName = serializers.CharField(source='CustomerID.Name', read_only=True)
    CompanyName = serializers.CharField(source='CompanyID.Name', read_only=True)
    # compatibility aliases (snake_case) — emit both forms during transition
    customer_name = serializers.CharField(source='CustomerID.Name', read_only=True)
    company_name = serializers.CharField(source='CompanyID.Name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'InvoiceID', 'InvoiceNumber', 'InvoiceDate', 'DueDate', 'TotalAmount',
            'Status', 'InvoiceNotes', 'CurrencyCode', 'CreatedDate',
            'CustomerName', 'CompanyName'
        ]
        read_only_fields = ['InvoiceID', 'CreatedDate']