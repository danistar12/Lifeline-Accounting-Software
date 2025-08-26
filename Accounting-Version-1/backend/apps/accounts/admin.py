from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, UserCompanyRole

class CustomUserAdmin(UserAdmin):
    model = User
    
    # Add the custom field to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_notes',)}),
    )
    
    # Add the custom field to the add_fieldsets (for creating new users)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_notes',)}),
    )

# Register models with admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(UserCompanyRole)
