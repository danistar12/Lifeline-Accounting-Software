from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, UserCompanyRole, UserSettings


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

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('UserID', 'EmailNotifications', 'DesktopNotifications', 'Theme', 'AutoSaveForms', 'DefaultCompany', 'ModifiedDate')
    list_filter = ('EmailNotifications', 'DesktopNotifications', 'Theme', 'TwoFactorEnabled')
    search_fields = ('UserID__username', 'UserID__email')
    readonly_fields = ('CreatedDate', 'ModifiedDate', 'LastExportDate')
    fieldsets = (
        ('User', {
            'fields': ('UserID',)
        }),
        ('Notification Preferences', {
            'fields': ('EmailNotifications', 'DesktopNotifications', 'NotificationTypes')
        }),
        ('Application Preferences', {
            'fields': ('AutoSaveForms', 'DefaultCompany', 'DateFormat', 'CurrencyFormat', 'Theme')
        }),
        ('Security', {
            'fields': ('TwoFactorEnabled', 'SessionTimeout')
        }),
        ('Data Export', {
            'fields': ('LastExportDate',)
        }),
        ('Timestamps', {
            'fields': ('CreatedDate', 'ModifiedDate'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(User, CustomUserAdmin)
