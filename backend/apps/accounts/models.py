from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    회원 모델 (Django User 확장)
    - 프론트엔드: join/membership.html
    """
    TIER_CHOICES = [
        ('FREE', '무료회원'),     # 무료 (기본)
        ('L1', '일반회원'),       # 연 30,000원
        ('L2', '후원회원'),       # 연 100,000원
        ('L3', '평생회원'),       # 500,000원
        ('SPECIAL', '특별회원'),  # 운영진/임원
    ]

    SOCIAL_PROVIDER_CHOICES = [
        ('', '일반'),
        ('kakao', '카카오'),
        ('naver', '네이버'),
        ('google', '구글'),
    ]

    JOIN_SOURCE_CHOICES = [
        ('search', '인터넷 검색'),
        ('sns', 'SNS'),
        ('recommend', '지인 추천'),
        ('event', '행사 참여'),
        ('news', '언론 보도'),
        ('other', '기타'),
    ]

    tier = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        default='FREE',
        verbose_name='회원등급'
    )
    tier_expires_at = models.DateField(null=True, blank=True, verbose_name='등급만료일')
    email_verified = models.BooleanField(default=False, verbose_name='이메일인증')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='활동명')
    phone = models.CharField(max_length=11, verbose_name='연락처')
    address = models.TextField(blank=True, verbose_name='주소')
    birth_date = models.DateField(null=True, blank=True, verbose_name='생년월일')
    occupation = models.CharField(max_length=100, blank=True, verbose_name='직업/소속')

    join_source = models.CharField(
        max_length=20,
        choices=JOIN_SOURCE_CHOICES,
        blank=True,
        verbose_name='가입경로'
    )
    join_message = models.TextField(blank=True, verbose_name='가입동기')

    is_donor = models.BooleanField(default=False, verbose_name='CMS후원여부')
    marketing_agreed = models.BooleanField(default=False, verbose_name='마케팅수신동의')

    social_provider = models.CharField(
        max_length=20,
        choices=SOCIAL_PROVIDER_CHOICES,
        blank=True,
        verbose_name='소셜로그인'
    )
    social_id = models.CharField(max_length=100, blank=True, verbose_name='소셜ID')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원 관리'

    def __str__(self):
        return f"{self.username} ({self.get_tier_display()})"

    @property
    def is_paid_member(self):
        """유료 회원 여부"""
        return self.tier in ['L1', 'L2', 'L3', 'SPECIAL']

    @property
    def is_special(self):
        """특별회원(운영진) 여부"""
        return self.tier == 'SPECIAL'

    @property
    def tier_price(self):
        """등급별 가격"""
        prices = {
            'FREE': 0,
            'L1': 30000,
            'L2': 100000,
            'L3': 500000,
            'SPECIAL': 0,
        }
        return prices.get(self.tier, 0)
