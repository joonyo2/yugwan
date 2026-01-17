from django.contrib import admin
from .models import Popup


@admin.register(Popup)
class PopupAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_at', 'end_at', 'is_active', 'is_visible', 'created_at']
    list_filter = ['is_active', 'start_at', 'end_at']
    search_fields = ['title']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'link_url')
        }),
        ('이미지', {
            'fields': ('pc_image', 'mobile_image')
        }),
        ('노출 설정', {
            'fields': ('start_at', 'end_at', 'is_active')
        }),
    )
