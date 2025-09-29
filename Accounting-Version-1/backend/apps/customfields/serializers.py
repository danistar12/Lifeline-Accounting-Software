from rest_framework import serializers
from .models import CustomField, CustomFieldValue

class CustomFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='CustomFieldID', read_only=True)
    company_id = serializers.IntegerField(source='CompanyID', read_only=True)
    field_name = serializers.CharField(source='FieldName')
    field_type = serializers.CharField(source='FieldType')
    table_name = serializers.CharField(source='TableName')
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    
    class Meta:
        model = CustomField
        fields = ('id', 'company_id', 'field_name', 'field_type', 'table_name', 'created_date')
        read_only_fields = ('id', 'created_date')

class CustomFieldValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ValueID', read_only=True)
    custom_field_id = serializers.IntegerField(source='CustomFieldID', read_only=True)
    record_id = serializers.IntegerField(source='RecordID')
    value = serializers.CharField()
    created_date = serializers.DateTimeField(source='CreatedDate', read_only=True)
    
    class Meta:
        model = CustomFieldValue
        fields = ('id', 'custom_field_id', 'record_id', 'value', 'created_date')
        read_only_fields = ('id', 'created_date')