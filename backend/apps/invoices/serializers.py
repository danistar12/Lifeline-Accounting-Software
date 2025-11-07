from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    CustomerName = serializers.SerializerMethodField()
    CompanyName = serializers.SerializerMethodField()
    # compatibility aliases (snake_case) — emit both forms during transition
    customer_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    def _get_customer_name(self, obj):
        customer = getattr(obj, 'CustomerID', None)
        return getattr(customer, 'Name', None)

    def _get_company_name(self, obj):
        company = getattr(obj, 'CompanyID', None)
        return getattr(company, 'CompanyName', None)

    def get_CustomerName(self, obj):
        return self._get_customer_name(obj)

    def get_customer_name(self, obj):
        return self._get_customer_name(obj)

    def get_CompanyName(self, obj):
        return self._get_company_name(obj)

    def get_company_name(self, obj):
        return self._get_company_name(obj)

    class Meta:
        model = Invoice
        fields = [
            'InvoiceID', 'CompanyID', 'CustomerID', 'InvoiceNumber', 'InvoiceDate', 'DueDate',
            'TotalAmount', 'Status', 'InvoiceNotes', 'CurrencyCode', 'CreatedDate',
            'CustomerName', 'CompanyName', 'customer_name', 'company_name'
        ]
        read_only_fields = ['InvoiceID', 'CreatedDate']