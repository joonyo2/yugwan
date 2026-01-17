from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'tier', 'phone', 'is_donor', 'created_at']
    list_filter = ['tier', 'is_donor', 'is_active', 'join_source']
    search_fields = ['username', 'email', 'phone', 'first_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('회원 정보', {
            'fields': ('tier', 'nickname', 'phone', 'address', 'birth_date', 'occupation')
        }),
        ('가입 정보', {
            'fields': ('join_source', 'join_message', 'is_donor', 'marketing_agreed', 'social_provider')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('회원 정보', {
            'fields': ('tier', 'phone', 'email')
        }),
    )
