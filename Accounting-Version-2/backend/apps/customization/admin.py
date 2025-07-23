from django.contrib import admin
from .models import CustomField, CustomFieldValue

# Register your models here.
admin.site.register(CustomField)
admin.site.register(CustomFieldValue)
