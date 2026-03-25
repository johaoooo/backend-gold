from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_verified_kyc', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_verified_kyc', 'is_staff')
    list_editable = ('is_approved',)  # Maintenant is_approved est dans list_display ✅
    fieldsets = UserAdmin.fieldsets + (
        ('Golden Invest', {'fields': ('role', 'phone', 'is_verified_kyc', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Golden Invest', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
