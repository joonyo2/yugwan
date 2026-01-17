from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from .models import VolunteerApplication, Donation


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'is_confirmed', 'created_at']
    list_filter = ['is_confirmed', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['is_confirmed']
    readonly_fields = ['created_at']
    actions = ['export_to_excel', 'mark_as_confirmed']

    @admin.action(description='선택한 신청서 엑셀 다운로드')
    def export_to_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "자원봉사 신청"

        headers = ['이름', '연락처', '이메일', '직업', '프로그램', '가능일정', '신청일']
        ws.append(headers)

        for app in queryset:
            ws.append([
                app.name, app.phone, app.email, app.occupation,
                ', '.join(app.programs) if app.programs else '',
                app.available_dates,
                app.created_at.strftime('%Y-%m-%d')
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=volunteer_applications.xlsx'
        wb.save(response)
        return response

    @admin.action(description='선택한 신청서 승인 처리')
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f'{updated}건이 승인 처리되었습니다.')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor_name', 'donation_type', 'amount', 'is_confirmed', 'created_at']
    list_filter = ['donation_type', 'is_confirmed', 'receipt_requested', 'created_at']
    search_fields = ['donor_name', 'phone', 'email']
    list_editable = ['is_confirmed']
    readonly_fields = ['created_at', 'confirmed_at']
    actions = ['export_to_excel', 'mark_as_confirmed']

    @admin.action(description='선택한 후원 엑셀 다운로드')
    def export_to_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "후원 내역"

        headers = ['후원자명', '유형', '금액', '연락처', '이메일', '영수증요청', '입금확인', '신청일']
        ws.append(headers)

        for d in queryset:
            ws.append([
                d.donor_name, d.get_donation_type_display(), d.amount,
                d.phone, d.email, '요청' if d.receipt_requested else '',
                '확인' if d.is_confirmed else '대기',
                d.created_at.strftime('%Y-%m-%d')
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=donations.xlsx'
        wb.save(response)
        return response

    @admin.action(description='선택한 후원 입금확인 처리')
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(is_confirmed=True, confirmed_at=timezone.now())
        self.message_user(request, f'{updated}건이 입금확인 처리되었습니다.')
