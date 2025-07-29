from rest_framework import serializers
from .models import Inventory, InventoryLocation, InvoiceLineItem, BillLineItem

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLocation
        fields = '__all__'

class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = '__all__'

class BillLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillLineItem
        fields = '__all__'
