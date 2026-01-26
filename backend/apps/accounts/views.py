from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, BoardPermission
from .serializers import UserSerializer, UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    회원가입 API
    - 모든 회원은 무료회원(FREE)으로 가입
    - 가입 즉시 승인 (is_active=True)
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user_id': user.id,
            'tier': user.tier,
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """내 정보 조회/수정 API"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """비밀번호 변경 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response(
                {'detail': '현재 비밀번호가 일치하지 않습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response({'message': '비밀번호가 변경되었습니다.'})


class AccountDeleteView(APIView):
    """회원 탈퇴 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get('password')
        user = request.user

        if not user.check_password(password):
            return Response(
                {'detail': '비밀번호가 일치하지 않습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()
        return Response({'message': '회원 탈퇴가 완료되었습니다.'})


# ========================================
# 관리자 전용 API
# ========================================

class SupporterApprovalView(APIView):
    """
    후원회원 승인 API (관리자 전용)
    - 운영진이 후원 확인 후 회원을 후원회원으로 승급
    """
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': '회원을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if target_user.tier == 'SUPPORTER':
            return Response(
                {'detail': '이미 후원회원입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_user.tier = 'SUPPORTER'
        target_user.tier_approved_at = timezone.now()
        target_user.tier_approved_by = request.user
        target_user.save()

        return Response({
            'message': f'{target_user.username}님이 후원회원으로 승급되었습니다.',
            'user_id': target_user.id,
            'tier': target_user.tier,
            'approved_at': target_user.tier_approved_at,
        })


class SupporterRevokeView(APIView):
    """
    후원회원 해제 API (관리자 전용)
    - 후원회원을 무료회원으로 변경
    """
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': '회원을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if target_user.tier == 'FREE':
            return Response(
                {'detail': '이미 무료회원입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_user.tier = 'FREE'
        target_user.tier_approved_at = None
        target_user.tier_approved_by = None
        target_user.save()

        return Response({
            'message': f'{target_user.username}님이 무료회원으로 변경되었습니다.',
            'user_id': target_user.id,
            'tier': target_user.tier,
        })


class UserListView(generics.ListAPIView):
    """
    회원 목록 조회 API (관리자 전용)
    - 전체 회원 목록 조회
    - 필터: tier, is_staff
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')

        # 필터링
        tier = self.request.query_params.get('tier')
        if tier:
            queryset = queryset.filter(tier=tier)

        is_staff = self.request.query_params.get('is_staff')
        if is_staff:
            queryset = queryset.filter(is_staff=is_staff.lower() == 'true')

        return queryset


class StaffAssignView(APIView):
    """
    운영진 지정 API (최고관리자 전용)
    """
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        # 최고관리자만 가능
        if not request.user.is_superuser:
            return Response(
                {'detail': '최고관리자만 운영진을 지정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': '회원을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        target_user.is_staff = True
        target_user.save()

        return Response({
            'message': f'{target_user.username}님이 운영진으로 지정되었습니다.',
            'user_id': target_user.id,
            'is_staff': target_user.is_staff,
        })


class StaffRevokeView(APIView):
    """
    운영진 해제 API (최고관리자 전용)
    """
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        # 최고관리자만 가능
        if not request.user.is_superuser:
            return Response(
                {'detail': '최고관리자만 운영진을 해제할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': '회원을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if target_user.is_superuser:
            return Response(
                {'detail': '최고관리자는 해제할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_user.is_staff = False
        target_user.save()

        return Response({
            'message': f'{target_user.username}님의 운영진 권한이 해제되었습니다.',
            'user_id': target_user.id,
            'is_staff': target_user.is_staff,
        })


# ========================================
# 게시판 권한 API
# ========================================

class BoardPermissionListView(generics.ListAPIView):
    """게시판 권한 설정 목록"""
    permission_classes = [IsAdminUser]
    queryset = BoardPermission.objects.all()

    def list(self, request, *args, **kwargs):
        permissions = BoardPermission.objects.all()
        data = [{
            'board_type': p.board_type,
            'board_name': p.get_board_type_display(),
            'read_permission': p.read_permission,
            'write_permission': p.write_permission,
            'is_active': p.is_active,
        } for p in permissions]
        return Response(data)


class BoardPermissionUpdateView(APIView):
    """게시판 권한 설정 수정 (관리자 전용)"""
    permission_classes = [IsAdminUser]

    def post(self, request, board_type):
        perm, created = BoardPermission.objects.get_or_create(board_type=board_type)

        read_permission = request.data.get('read_permission')
        write_permission = request.data.get('write_permission')
        is_active = request.data.get('is_active')

        if read_permission:
            perm.read_permission = read_permission
        if write_permission:
            perm.write_permission = write_permission
        if is_active is not None:
            perm.is_active = is_active

        perm.save()

        return Response({
            'message': f'{perm.get_board_type_display()} 권한이 수정되었습니다.',
            'board_type': perm.board_type,
            'read_permission': perm.read_permission,
            'write_permission': perm.write_permission,
        })


class CheckBoardPermissionView(APIView):
    """
    게시판 접근 권한 확인 API
    - 프론트엔드에서 게시판 접근 전 권한 확인용
    """
    permission_classes = [AllowAny]

    def get(self, request, board_type):
        user = request.user

        can_read = BoardPermission.check_read_permission(board_type, user)
        can_write = BoardPermission.check_write_permission(board_type, user)

        return Response({
            'board_type': board_type,
            'can_read': can_read,
            'can_write': can_write,
            'user_tier': user.tier if user.is_authenticated else None,
            'is_admin': user.is_admin if user.is_authenticated else False,
        })
