from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('budget_id', 'company', 'account', 'budget_year', 'budget_month', 'amount')
    list_filter = ('budget_year', 'budget_month')
    search_fields = ('description', 'budget_notes')
