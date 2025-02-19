from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
        (_('Additional Info'), {
            'fields': ('email_verified', 'phone_number_verified', 'two_factor_enabled', 'two_factor_type', 'available_balance', 'user_number'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Additional Info'), {
            'fields': ('email_verified', 'phone_number_verified', 'two_factor_enabled', 'two_factor_type', 'available_balance'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'user_number')

admin.site.register(CustomUser, CustomUserAdmin)
