from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import ContestApplication


@admin.register(ContestApplication)
class ContestApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_name', 'division', 'grade', 'status', 'created_at']
    list_filter = ['contest_year', 'division', 'status', 'grade']
    search_fields = ['name', 'contact_parent', 'school_name', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['export_to_excel', 'mark_as_accepted', 'mark_as_rejected']

    fieldsets = (
        ('대회 정보', {
            'fields': ('contest_year',)
        }),
        ('참가자 정보', {
            'fields': ('name', 'birth_date', 'school_name', 'grade')
        }),
        ('참가 부문', {
            'fields': ('division', 'speech_title', 'script_file')
        }),
        ('연락처', {
            'fields': ('parent_name', 'contact_parent', 'teacher_name', 'email', 'address')
        }),
        ('처리 상태', {
            'fields': ('status', 'admin_memo', 'reject_reason')
        }),
        ('동의 사항', {
            'fields': ('rules_agreed', 'privacy_agreed', 'news_agreed'),
            'classes': ('collapse',)
        }),
        ('시스템', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description='선택한 신청서 엑셀 다운로드')
    def export_to_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "웅변대회 신청자"

        headers = ['접수번호', '성명', '학교', '학년', '부문', '제목', '보호자', '연락처', '이메일', '접수일']
        ws.append(headers)

        for app in queryset:
            ws.append([
                app.receipt_number,
                app.name,
                app.school_name,
                app.get_grade_display(),
                app.get_division_display(),
                app.speech_title,
                app.parent_name,
                app.contact_parent,
                app.email,
                app.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f'contest_applications_{queryset.first().contest_year if queryset.exists() else "all"}.xlsx'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        wb.save(response)
        return response

    @admin.action(description='선택한 신청서 참가확정 처리')
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='ACCEPTED')
        self.message_user(request, f'{updated}건이 참가확정 처리되었습니다.')

    @admin.action(description='선택한 신청서 반려 처리')
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'{updated}건이 반려 처리되었습니다.')
