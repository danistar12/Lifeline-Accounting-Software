from django.contrib import admin
from .models import User, UserCompanyRole, ChartOfAccounts, GeneralLedger

admin.site.register(User)
admin.site.register(UserCompanyRole)
admin.site.register(ChartOfAccounts)
admin.site.register(GeneralLedger)
