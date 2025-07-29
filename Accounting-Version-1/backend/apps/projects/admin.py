from django.contrib import admin
from .models import Project, TimeEntry

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'company', 'customer', 'start_date', 'end_date', 'status')
    search_fields = ('project_name', 'project_notes')
    list_filter = ('status', 'start_date', 'end_date')

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('project', 'employee', 'work_date', 'hours', 'billable')
    search_fields = ('time_entry_notes',)
    list_filter = ('work_date', 'billable')
