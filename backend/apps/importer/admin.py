from django.contrib import admin
from .models import ImportFile, ImportError

@admin.register(ImportFile)
class ImportFileAdmin(admin.ModelAdmin):
	list_display = ('id', 'CompanyID', 'FileType', 'File', 'UploadedAt', 'Status')
	search_fields = ('File', 'Status')

@admin.register(ImportError)
class ImportErrorAdmin(admin.ModelAdmin):
	list_display = ('id', 'ImportFileID', 'RowNumber', 'ErrorMessage')
	search_fields = ('ErrorMessage',)
