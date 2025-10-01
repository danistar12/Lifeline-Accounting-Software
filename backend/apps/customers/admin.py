from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'Phone', 'CompanyID', 'CreatedDate')
    list_filter = ('CompanyID', 'CreatedDate')
    search_fields = ('Name', 'Email', 'Phone')
    ordering = ('-CreatedDate',)
