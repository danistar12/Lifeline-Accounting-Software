from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'VendorID', 'CompanyID', 'Name', 'Email', 'Phone',
            'Address', 'PaymentTerms', 'VendorNotes', 'CreatedDate'
        ]
        read_only_fields = ['VendorID', 'CreatedDate']