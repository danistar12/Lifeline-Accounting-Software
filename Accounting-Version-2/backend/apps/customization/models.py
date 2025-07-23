from django.db import models
from apps.core.models import Company

class CustomField(models.Model):
    custom_field_id = models.AutoField(primary_key=True, db_column='CustomFieldID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='CompanyID')
    field_name = models.CharField(max_length=100, db_column='FieldName')
    field_type = models.CharField(max_length=50, db_column='FieldType')  # e.g., 'Text', 'Number', 'Date'
    table_name = models.CharField(max_length=100, db_column='TableName')  # e.g., 'Customers', 'Vendors'
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.table_name} - {self.field_name}"

    class Meta:
        db_table = 'CustomFields'

class CustomFieldValue(models.Model):
    value_id = models.AutoField(primary_key=True, db_column='ValueID')
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE, db_column='CustomFieldID')
    record_id = models.IntegerField(db_column='RecordID')  # ID of the record in the table_name table
    value = models.TextField(db_column='Value')  # Stored as text regardless of field_type
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    def __str__(self):
        return f"{self.custom_field.field_name}: {self.value}"

    class Meta:
        db_table = 'CustomFieldValues'
