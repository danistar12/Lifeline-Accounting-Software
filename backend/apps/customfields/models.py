from django.db import models
from apps.accounts.models import Company

class CustomField(models.Model):
    CustomFieldID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    FieldName = models.CharField(max_length=255)
    FieldType = models.CharField(max_length=50)
    TableName = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.FieldName} ({self.TableName})"

    class Meta:
        db_table = 'CustomFields'


class CustomFieldValue(models.Model):
    ValueID = models.AutoField(primary_key=True)
    CustomFieldID = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    RecordID = models.IntegerField()
    Value = models.TextField()
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.CustomFieldID.FieldName}: {self.Value}"

    class Meta:
        db_table = 'CustomFieldValues'
