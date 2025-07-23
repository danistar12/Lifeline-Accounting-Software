from django.contrib import admin
from .models import Company, ChartOfAccounts, GeneralLedger

admin.site.register(Company)
admin.site.register(ChartOfAccounts)
admin.site.register(GeneralLedger)
