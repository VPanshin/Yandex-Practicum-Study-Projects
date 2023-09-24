from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('pk', 'username', 'email', 'role',
                    'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'role', 'is_staff', 'is_active',)
    search_fields = ('email',)
    empty_value_display = '-пусто-'
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',
                'first_name', 'last_name', 'bio', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


admin.site.register(User, CustomUserAdmin)
