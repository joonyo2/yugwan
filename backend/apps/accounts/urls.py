from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # JWT 토큰 (로그인)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 회원가입/탈퇴
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('delete/', views.AccountDeleteView.as_view(), name='delete'),

    # 내 정보
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),

    # 관리자: 회원 관리
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/approve-supporter/', views.SupporterApprovalView.as_view(), name='approve_supporter'),
    path('users/<int:user_id>/revoke-supporter/', views.SupporterRevokeView.as_view(), name='revoke_supporter'),
    path('users/<int:user_id>/assign-staff/', views.StaffAssignView.as_view(), name='assign_staff'),
    path('users/<int:user_id>/revoke-staff/', views.StaffRevokeView.as_view(), name='revoke_staff'),

    # 게시판 권한
    path('board-permissions/', views.BoardPermissionListView.as_view(), name='board_permissions'),
    path('board-permissions/<str:board_type>/', views.BoardPermissionUpdateView.as_view(), name='board_permission_update'),
    path('check-permission/<str:board_type>/', views.CheckBoardPermissionView.as_view(), name='check_permission'),
]
