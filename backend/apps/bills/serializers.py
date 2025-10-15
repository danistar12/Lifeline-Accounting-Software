from rest_framework import serializers
from apps.accounts.models import Company
from apps.vendors.models import Vendor
from .models import Bill


class VendorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['VendorID', 'Name', 'Email', 'Phone']
        read_only_fields = ['VendorID']


class BillSerializer(serializers.ModelSerializer):
    CompanyID = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    VendorID = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    UserID = serializers.PrimaryKeyRelatedField(read_only=True)
    Vendor = VendorSummarySerializer(source='VendorID', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'BillID', 'CompanyID', 'VendorID', 'Vendor',
            'BillNumber', 'BillDate', 'DueDate', 'TotalAmount',
            'Status', 'BillNotes', 'CurrencyCode', 'UserID',
            'CreatedDate', 'ModifiedDate',
        ]
        read_only_fields = ['BillID', 'CreatedDate', 'ModifiedDate']