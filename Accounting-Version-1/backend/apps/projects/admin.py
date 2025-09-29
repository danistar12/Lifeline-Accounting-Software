from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('ProjectName', 'CompanyID', 'CustomerID', 'StartDate', 'EndDate', 'Status')
    search_fields = ('ProjectName', 'ProjectNotes')
    list_filter = ('Status', 'StartDate', 'EndDate')
