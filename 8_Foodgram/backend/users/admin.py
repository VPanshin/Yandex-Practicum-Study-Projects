from django.contrib import admin

from users.models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'role')
    list_filter = ('email', 'first_name',)
    search_fields = ('email', 'first_name',)


admin.site.register(User, CustomUserAdmin)
