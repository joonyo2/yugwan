from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import User, BoardPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'tier', 'admin_level',
        'phone', 'is_active', 'created_at'
    ]
    list_filter = ['tier', 'admin_level', 'is_staff', 'is_superuser', 'is_active', 'join_source']
    search_fields = ['username', 'email', 'phone', 'first_name']
    ordering = ['-created_at']

    # 후원회원 승인 액션
    actions = ['approve_as_supporter', 'revoke_supporter', 'assign_staff', 'revoke_staff']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('회원 등급', {
            'fields': ('tier', 'tier_approved_at', 'tier_approved_by', 'admin_level')
        }),
        ('회원 정보', {
            'fields': ('phone', 'address', 'birth_date', 'occupation')
        }),
        ('가입 정보', {
            'fields': ('join_source', 'join_message', 'marketing_agreed')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('회원 정보', {
            'fields': ('phone', 'email')
        }),
    )

    readonly_fields = ['tier_approved_at', 'tier_approved_by', 'admin_level']

    @admin.action(description='선택한 회원을 후원회원으로 승급')
    def approve_as_supporter(self, request, queryset):
        count = 0
        for user in queryset:
            if user.tier != 'SUPPORTER':
                user.tier = 'SUPPORTER'
                user.tier_approved_at = timezone.now()
                user.tier_approved_by = request.user
                user.save()
                count += 1
        self.message_user(request, f'{count}명의 회원이 후원회원으로 승급되었습니다.')

    @admin.action(description='선택한 회원의 후원회원 자격 해제')
    def revoke_supporter(self, request, queryset):
        count = queryset.filter(tier='SUPPORTER').update(
            tier='FREE',
            tier_approved_at=None,
            tier_approved_by=None
        )
        self.message_user(request, f'{count}명의 회원이 무료회원으로 변경되었습니다.')

    @admin.action(description='선택한 회원을 운영진으로 지정')
    def assign_staff(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, '최고관리자만 운영진을 지정할 수 있습니다.', level='error')
            return
        count = queryset.update(is_staff=True)
        self.message_user(request, f'{count}명의 회원이 운영진으로 지정되었습니다.')

    @admin.action(description='선택한 회원의 운영진 권한 해제')
    def revoke_staff(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, '최고관리자만 운영진 권한을 해제할 수 있습니다.', level='error')
            return
        # 최고관리자는 해제 불가
        count = queryset.filter(is_superuser=False).update(is_staff=False)
        self.message_user(request, f'{count}명의 회원의 운영진 권한이 해제되었습니다.')


@admin.register(BoardPermission)
class BoardPermissionAdmin(admin.ModelAdmin):
    list_display = ['board_type', 'get_board_name', 'read_permission', 'write_permission', 'is_active']
    list_filter = ['read_permission', 'write_permission', 'is_active']
    list_editable = ['read_permission', 'write_permission', 'is_active']

    def get_board_name(self, obj):
        return obj.get_board_type_display()
    get_board_name.short_description = '게시판명'
