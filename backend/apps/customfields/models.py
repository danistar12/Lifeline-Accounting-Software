from django.db import models
from apps.accounts.models import Company

class CustomField(models.Model):
    CustomFieldID = models.AutoField(primary_key=True, verbose_name="Custom Field ID")
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Company")
    FieldName = models.CharField(max_length=255, verbose_name="Field Name")
    FieldType = models.CharField(max_length=50, verbose_name="Field Type")
    TableName = models.CharField(max_length=255, verbose_name="Table Name")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.FieldName} ({self.TableName})"

    class Meta:
        db_table = 'CustomFields'
        verbose_name = "Custom Field"
        verbose_name_plural = "Custom Fields"


class CustomFieldValue(models.Model):
    ValueID = models.AutoField(primary_key=True, verbose_name="Value ID")
    CustomFieldID = models.ForeignKey(CustomField, on_delete=models.CASCADE, verbose_name="Custom Field")
    RecordID = models.IntegerField(verbose_name="Record ID")
    Value = models.TextField(verbose_name="Value")
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.CustomFieldID.FieldName}: {self.Value}"

    class Meta:
        db_table = 'CustomFieldValues'
        verbose_name = "Custom Field Value"
        verbose_name_plural = "Custom Field Values"
