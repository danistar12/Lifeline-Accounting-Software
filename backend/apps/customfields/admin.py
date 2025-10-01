from django.contrib import admin
from .models import CustomField, CustomFieldValue

@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
	list_display = ('CustomFieldID', 'CompanyID', 'FieldName', 'FieldType', 'TableName', 'CreatedDate')
	search_fields = ('FieldName', 'TableName')

@admin.register(CustomFieldValue)
class CustomFieldValueAdmin(admin.ModelAdmin):
	list_display = ('ValueID', 'CustomFieldID', 'RecordID', 'Value', 'CreatedDate')
	search_fields = ('Value',)
