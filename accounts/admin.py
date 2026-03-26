from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .utils import send_account_approved_email

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_verified_kyc', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_verified_kyc', 'is_staff')
    list_editable = ('is_approved',)
    fieldsets = UserAdmin.fieldsets + (
        ('Golden Invest', {'fields': ('role', 'phone', 'is_verified_kyc', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Golden Invest', {'fields': ('role', 'phone')}),
    )

    def save_model(self, request, obj, form, change):
        if change and 'is_approved' in form.changed_data:
            old_obj = self.model.objects.get(pk=obj.pk)
            if not old_obj.is_approved and obj.is_approved:
                send_account_approved_email(obj)
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
