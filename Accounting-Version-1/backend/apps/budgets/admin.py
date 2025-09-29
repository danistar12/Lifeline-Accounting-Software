from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('BudgetID', 'CompanyID', 'AccountID', 'BudgetYear', 'BudgetMonth', 'Amount')
    list_filter = ('BudgetYear', 'BudgetMonth')
    search_fields = ('Description', 'BudgetNotes')
