from rest_framework import serializers
from apps.accounts.models import Company
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    CompanyID = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Customer
        fields = [
            'CustomerID',
            'CompanyID',
            'Name',
            'Email',
            'Phone',
            'Address',
            'PaymentTerms',
            'CustomerNotes',
            'CreatedDate',
        ]
        read_only_fields = ['CustomerID', 'CreatedDate']