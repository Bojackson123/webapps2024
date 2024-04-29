from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

    
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'balance', 'currency')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'balance', 'currency'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'balance', 'currency', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
