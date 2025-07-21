from django.contrib import admin
from .models import User, Company, UserCompanyRole

admin.site.register(User)
admin.site.register(Company)
admin.site.register(UserCompanyRole)
