from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, User


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username', 'is_active', 'user_type',)
    ordering = ('-created_at',)
    list_display = ('email', 'username', 'is_active', 'is_staff', 'user_type',)

    fieldsets = (
        (None, {'fields': ('email', 'username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'email_verified')}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type', 'is_active',)
        }),
    )


admin.site.register(CustomUser, UserAdminConfig)


@admin.register(User)
class AdminOrder(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'email_verified']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'email_verified']
    ordering = ['created_at']
