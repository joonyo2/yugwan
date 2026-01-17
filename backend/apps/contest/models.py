from django.db import models
from .validators import validate_script_file


class ContestApplication(models.Model):
    """
    웅변대회 참가 신청서
    - 프론트엔드: contest/apply.html
    """
    DIVISION_CHOICES = [
        ('korean', '한국어 웅변'),
        ('english', '영어 웅변'),
    ]

    GRADE_CHOICES = [
        ('초4', '초등학교 4학년'),
        ('초5', '초등학교 5학년'),
        ('초6', '초등학교 6학년'),
        ('중1', '중학교 1학년'),
        ('중2', '중학교 2학년'),
        ('중3', '중학교 3학년'),
        ('고1', '고등학교 1학년'),
        ('고2', '고등학교 2학년'),
        ('고3', '고등학교 3학년'),
    ]

    STATUS_CHOICES = [
        ('SUBMITTED', '접수완료'),
        ('CHECKING', '서류검토중'),
        ('ACCEPTED', '참가확정'),
        ('REJECTED', '반려'),
    ]

    # 대회 정보
    contest_year = models.IntegerField(verbose_name='대회연도')

    # 참가자 정보
    name = models.CharField(max_length=50, verbose_name='참가자 성명')
    birth_date = models.DateField(verbose_name='생년월일')
    school_name = models.CharField(max_length=100, verbose_name='학교명')
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, verbose_name='학년')

    # 참가 부문
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, verbose_name='참가부문')
    speech_title = models.CharField(max_length=200, verbose_name='웅변 제목')

    # 연락처 정보
    parent_name = models.CharField(max_length=50, verbose_name='보호자 성함')
    contact_parent = models.CharField(max_length=11, verbose_name='보호자 연락처')
    teacher_name = models.CharField(max_length=50, blank=True, verbose_name='지도교사')
    email = models.EmailField(verbose_name='이메일')
    address = models.CharField(max_length=200, blank=True, verbose_name='주소')

    # 원고 파일
    script_file = models.FileField(
        upload_to='contest/scripts/%Y/',
        validators=[validate_script_file],
        verbose_name='원고 파일'
    )

    # 상태 관리
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SUBMITTED',
        verbose_name='처리상태'
    )
    admin_memo = models.TextField(blank=True, verbose_name='관리자 메모')
    reject_reason = models.TextField(blank=True, verbose_name='반려 사유')

    # 동의 사항
    rules_agreed = models.BooleanField(default=False, verbose_name='참가요강 동의')
    privacy_agreed = models.BooleanField(default=False, verbose_name='개인정보 동의')
    news_agreed = models.BooleanField(default=False, verbose_name='소식수신 동의')

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='접수일시')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '웅변대회 신청서'
        verbose_name_plural = '웅변대회 신청서 관리'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.contest_year}] {self.name} - {self.get_division_display()}"

    @property
    def receipt_number(self):
        return f"{self.contest_year}-{self.id:04d}"
