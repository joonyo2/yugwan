from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    회원 모델 (Django User 확장)

    회원 등급:
    - FREE: 무료회원 (가입 즉시 승인)
    - SUPPORTER: 후원회원 (후원 후 관리자 승인 필요)

    관리자 등급:
    - is_superuser: 최고관리자 (Django 기본)
    - is_staff: 관리자/운영진 (Django 기본)
    """
    TIER_CHOICES = [
        ('FREE', '무료회원'),
        ('SUPPORTER', '후원회원'),
    ]

    ADMIN_LEVEL_CHOICES = [
        ('NONE', '일반회원'),
        ('STAFF', '운영진'),
        ('SUPER', '최고관리자'),
    ]

    JOIN_SOURCE_CHOICES = [
        ('search', '인터넷 검색'),
        ('sns', 'SNS'),
        ('recommend', '지인 추천'),
        ('event', '행사 참여'),
        ('news', '언론 보도'),
        ('other', '기타'),
    ]

    # 회원 등급
    tier = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        default='FREE',
        verbose_name='회원등급'
    )
    tier_approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='후원회원 승인일'
    )
    tier_approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users',
        verbose_name='승인 관리자'
    )

    # 관리자 레벨 (표시용)
    admin_level = models.CharField(
        max_length=10,
        choices=ADMIN_LEVEL_CHOICES,
        default='NONE',
        verbose_name='관리자등급'
    )

    # 기본 정보
    phone = models.CharField(max_length=11, verbose_name='연락처')
    address = models.TextField(blank=True, verbose_name='주소')
    birth_date = models.DateField(null=True, blank=True, verbose_name='생년월일')
    occupation = models.CharField(max_length=100, blank=True, verbose_name='직업/소속')

    # 가입 정보
    join_source = models.CharField(
        max_length=20,
        choices=JOIN_SOURCE_CHOICES,
        blank=True,
        verbose_name='가입경로'
    )
    join_message = models.TextField(blank=True, verbose_name='가입동기')
    marketing_agreed = models.BooleanField(default=False, verbose_name='마케팅수신동의')

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원 관리'

    def __str__(self):
        return f"{self.username} ({self.get_tier_display()})"

    def save(self, *args, **kwargs):
        # admin_level 자동 동기화
        if self.is_superuser:
            self.admin_level = 'SUPER'
        elif self.is_staff:
            self.admin_level = 'STAFF'
        else:
            self.admin_level = 'NONE'
        super().save(*args, **kwargs)

    @property
    def is_supporter(self):
        """후원회원 여부"""
        return self.tier == 'SUPPORTER'

    @property
    def is_admin(self):
        """관리자(운영진) 여부"""
        return self.is_staff or self.is_superuser

    def can_access_board(self, board):
        """게시판 접근 권한 확인"""
        # 관리자는 모든 게시판 접근 가능
        if self.is_admin:
            return True

        # 게시판의 required_tier 확인
        if hasattr(board, 'required_tier'):
            if board.required_tier == 'SUPPORTER' and self.tier != 'SUPPORTER':
                return False

        return True


class BoardPermission(models.Model):
    """
    게시판별 접근 권한 설정
    - 각 게시판(archive 앱의 모델들)에 대해 회원등급별 접근 권한 설정
    """
    BOARD_CHOICES = [
        ('notice', '공지사항'),
        ('news', '보도자료'),
        ('gallery', '갤러리'),
        ('video', '영상'),
        ('member_notice', '회원 공지'),  # 후원회원 전용
        ('member_resource', '회원 자료실'),  # 후원회원 전용
    ]

    PERMISSION_CHOICES = [
        ('ALL', '전체 공개'),
        ('FREE', '무료회원 이상'),
        ('SUPPORTER', '후원회원 전용'),
        ('ADMIN', '관리자 전용'),
    ]

    board_type = models.CharField(
        max_length=30,
        choices=BOARD_CHOICES,
        unique=True,
        verbose_name='게시판'
    )
    read_permission = models.CharField(
        max_length=20,
        choices=PERMISSION_CHOICES,
        default='ALL',
        verbose_name='읽기 권한'
    )
    write_permission = models.CharField(
        max_length=20,
        choices=PERMISSION_CHOICES,
        default='ADMIN',
        verbose_name='쓰기 권한'
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화')

    class Meta:
        verbose_name = '게시판 권한'
        verbose_name_plural = '게시판 권한 설정'

    def __str__(self):
        return f"{self.get_board_type_display()} - 읽기:{self.get_read_permission_display()}"

    @classmethod
    def check_read_permission(cls, board_type, user):
        """사용자의 게시판 읽기 권한 확인"""
        try:
            perm = cls.objects.get(board_type=board_type)
        except cls.DoesNotExist:
            return True  # 권한 설정 없으면 기본 공개

        if perm.read_permission == 'ALL':
            return True
        if perm.read_permission == 'FREE':
            return user.is_authenticated
        if perm.read_permission == 'SUPPORTER':
            return user.is_authenticated and (user.tier == 'SUPPORTER' or user.is_admin)
        if perm.read_permission == 'ADMIN':
            return user.is_authenticated and user.is_admin

        return False

    @classmethod
    def check_write_permission(cls, board_type, user):
        """사용자의 게시판 쓰기 권한 확인"""
        try:
            perm = cls.objects.get(board_type=board_type)
        except cls.DoesNotExist:
            return user.is_authenticated and user.is_admin

        if perm.write_permission == 'ALL':
            return user.is_authenticated
        if perm.write_permission == 'FREE':
            return user.is_authenticated
        if perm.write_permission == 'SUPPORTER':
            return user.is_authenticated and (user.tier == 'SUPPORTER' or user.is_admin)
        if perm.write_permission == 'ADMIN':
            return user.is_authenticated and user.is_admin

        return False
