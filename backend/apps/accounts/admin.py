from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, UserCompanyRole


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('UserNotes',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('UserNotes',)}),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('CompanyID', 'CompanyName', 'CompanyNotes', 'AdminUserID', 'CreatedDate')
    search_fields = ('CompanyName',)

@admin.register(UserCompanyRole)
class UserCompanyRoleAdmin(admin.ModelAdmin):
    list_display = ('UserCompanyRoleID', 'UserID', 'CompanyID', 'Role', 'CreatedDate')
    search_fields = ('Role',)

admin.site.register(User, CustomUserAdmin)
