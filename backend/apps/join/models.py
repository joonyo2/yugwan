from django.db import models


class VolunteerApplication(models.Model):
    """자원봉사 신청 - 프론트엔드: join/volunteer.html"""
    PROGRAM_CHOICES = [
        ('contest', '웅변대회 운영'),
        ('education', '역사교육 봉사'),
        ('memorial', '추모행사 지원'),
        ('office', '사무국 지원'),
    ]

    name = models.CharField(max_length=50, verbose_name='이름')
    birth_date = models.DateField(verbose_name='생년월일')
    phone = models.CharField(max_length=11, verbose_name='연락처')
    email = models.EmailField(verbose_name='이메일')
    occupation = models.CharField(max_length=100, verbose_name='직업/소속')

    programs = models.JSONField(verbose_name='참여 프로그램')
    available_dates = models.TextField(verbose_name='참여 가능 일정')
    experience = models.TextField(blank=True, verbose_name='관련 경험')
    motivation = models.TextField(verbose_name='지원 동기')

    privacy_agreed = models.BooleanField(default=False, verbose_name='개인정보동의')
    is_confirmed = models.BooleanField(default=False, verbose_name='승인여부')
    admin_memo = models.TextField(blank=True, verbose_name='관리자메모')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '자원봉사 신청'
        verbose_name_plural = '자원봉사 신청 관리'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class Donation(models.Model):
    """후원 신청 - 프론트엔드: join/donation.html"""
    TYPE_CHOICES = [
        ('once', '일시 후원'),
        ('monthly', '정기 후원'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='회원'
    )
    donation_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='후원유형')
    amount = models.IntegerField(verbose_name='후원금액')

    donor_name = models.CharField(max_length=50, verbose_name='후원자명')
    phone = models.CharField(max_length=11, verbose_name='연락처')
    email = models.EmailField(verbose_name='이메일')

    receipt_requested = models.BooleanField(default=False, verbose_name='영수증요청')
    receipt_name = models.CharField(max_length=50, blank=True, verbose_name='영수증 발급명')
    receipt_id = models.CharField(max_length=20, blank=True, verbose_name='주민/사업자번호')

    is_confirmed = models.BooleanField(default=False, verbose_name='입금확인')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='입금확인일시')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '후원'
        verbose_name_plural = '후원 관리'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name} - {self.amount:,}원"
