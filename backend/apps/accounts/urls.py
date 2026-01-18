from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegisterView, UserProfileView, PasswordChangeView,
    EmailVerificationSendView, EmailVerificationConfirmView,
    TierUpgradeRequestView, AccountDeleteView,
    KakaoLoginView, KakaoCallbackView,
    NaverLoginView, NaverCallbackView,
    GoogleLoginView, GoogleCallbackView,
    SocialUnlinkView
)

urlpatterns = [
    # 기본 인증
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # 비밀번호 & 이메일 인증
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('email/verify/send/', EmailVerificationSendView.as_view(), name='email-verify-send'),
    path('email/verify/', EmailVerificationConfirmView.as_view(), name='email-verify'),

    # 등급 업그레이드 & 탈퇴
    path('upgrade/request/', TierUpgradeRequestView.as_view(), name='tier-upgrade'),
    path('account/delete/', AccountDeleteView.as_view(), name='account-delete'),

    # 소셜 로그인 - 카카오
    path('social/kakao/', KakaoLoginView.as_view(), name='kakao-login'),
    path('social/kakao/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),

    # 소셜 로그인 - 네이버
    path('social/naver/', NaverLoginView.as_view(), name='naver-login'),
    path('social/naver/callback/', NaverCallbackView.as_view(), name='naver-callback'),

    # 소셜 로그인 - 구글
    path('social/google/', GoogleLoginView.as_view(), name='google-login'),
    path('social/google/callback/', GoogleCallbackView.as_view(), name='google-callback'),

    # 소셜 연동 해제
    path('social/<str:provider>/unlink/', SocialUnlinkView.as_view(), name='social-unlink'),
]
