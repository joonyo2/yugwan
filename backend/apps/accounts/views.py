import os
import random
import string
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    """회원가입 API"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user_id': user.id
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
            return Response({'detail': '현재 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': '비밀번호가 변경되었습니다.'})


class EmailVerificationSendView(APIView):
    """이메일 인증코드 발송 API"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': '이메일을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 인증 코드 생성 (6자리)
        code = ''.join(random.choices(string.digits, k=6))

        # 세션에 코드 저장 (실제로는 캐시나 DB에 저장)
        request.session['email_verification_code'] = code
        request.session['email_verification_email'] = email

        # TODO: 실제 이메일 발송 로직 구현
        # send_email(email, '인증 코드', f'인증 코드: {code}')

        return Response({'message': '인증 코드가 발송되었습니다.'})


class EmailVerificationConfirmView(APIView):
    """이메일 인증코드 확인 API"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        saved_code = request.session.get('email_verification_code')
        saved_email = request.session.get('email_verification_email')

        if saved_email != email or saved_code != code:
            return Response({'detail': '인증 코드가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 인증 성공 표시
        request.session['email_verified'] = email

        return Response({'message': '이메일이 인증되었습니다.'})


class TierUpgradeRequestView(APIView):
    """회원 등급 업그레이드 신청 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tier = request.data.get('tier')
        valid_tiers = ['L1', 'L2', 'L3']

        if tier not in valid_tiers:
            return Response({'detail': '유효하지 않은 등급입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: 업그레이드 신청 내역 저장 (별도 모델 필요)
        # 실제로는 결제 대기 상태로 저장하고 관리자가 입금 확인 후 등급 변경

        return Response({'message': f'{tier} 등급 업그레이드 신청이 완료되었습니다. 입금 확인 후 등급이 변경됩니다.'})


class AccountDeleteView(APIView):
    """회원 탈퇴 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get('password')
        user = request.user

        if not user.check_password(password):
            return Response({'detail': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({'message': '회원 탈퇴가 완료되었습니다.'})


# ========================================
# 소셜 로그인 API
# ========================================

class KakaoLoginView(APIView):
    """카카오 로그인 시작"""
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_uri = request.query_params.get('redirect_uri', '')
        client_id = os.getenv('KAKAO_CLIENT_ID', '')

        kakao_auth_url = (
            f"https://kauth.kakao.com/oauth/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
        )
        return redirect(kakao_auth_url)


class KakaoCallbackView(APIView):
    """카카오 로그인 콜백"""
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        redirect_uri = request.query_params.get('redirect_uri', '')
        client_id = os.getenv('KAKAO_CLIENT_ID', '')
        client_secret = os.getenv('KAKAO_CLIENT_SECRET', '')

        # 액세스 토큰 요청
        token_response = requests.post(
            'https://kauth.kakao.com/oauth/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'code': code
            }
        )
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        # 사용자 정보 요청
        user_response = requests.get(
            'https://kapi.kakao.com/v2/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        user_data = user_response.json()

        kakao_id = str(user_data.get('id'))
        kakao_account = user_data.get('kakao_account', {})
        email = kakao_account.get('email', f'kakao_{kakao_id}@yugwansun.org')
        nickname = kakao_account.get('profile', {}).get('nickname', '')

        # 사용자 생성 또는 조회
        user, created = User.objects.get_or_create(
            social_provider='kakao',
            social_id=kakao_id,
            defaults={
                'username': f'kakao_{kakao_id}',
                'email': email,
                'nickname': nickname,
                'email_verified': True,
            }
        )

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })


class NaverLoginView(APIView):
    """네이버 로그인 시작"""
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_uri = request.query_params.get('redirect_uri', '')
        client_id = os.getenv('NAVER_CLIENT_ID', '')
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        naver_auth_url = (
            f"https://nid.naver.com/oauth2.0/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&state={state}"
        )
        return redirect(naver_auth_url)


class NaverCallbackView(APIView):
    """네이버 로그인 콜백"""
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        client_id = os.getenv('NAVER_CLIENT_ID', '')
        client_secret = os.getenv('NAVER_CLIENT_SECRET', '')

        # 액세스 토큰 요청
        token_response = requests.post(
            'https://nid.naver.com/oauth2.0/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'state': state
            }
        )
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        # 사용자 정보 요청
        user_response = requests.get(
            'https://openapi.naver.com/v1/nid/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        user_data = user_response.json().get('response', {})

        naver_id = user_data.get('id')
        email = user_data.get('email', f'naver_{naver_id}@yugwansun.org')
        nickname = user_data.get('nickname', '')
        name = user_data.get('name', '')
        phone = user_data.get('mobile', '').replace('-', '')

        # 사용자 생성 또는 조회
        user, created = User.objects.get_or_create(
            social_provider='naver',
            social_id=naver_id,
            defaults={
                'username': f'naver_{naver_id}',
                'email': email,
                'nickname': nickname,
                'first_name': name,
                'phone': phone,
                'email_verified': True,
            }
        )

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })


class GoogleLoginView(APIView):
    """구글 로그인 시작"""
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_uri = request.query_params.get('redirect_uri', '')
        client_id = os.getenv('GOOGLE_CLIENT_ID', '')

        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=email%20profile"
        )
        return redirect(google_auth_url)


class GoogleCallbackView(APIView):
    """구글 로그인 콜백"""
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        redirect_uri = request.query_params.get('redirect_uri', '')
        client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')

        # 액세스 토큰 요청
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'code': code
            }
        )
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        # 사용자 정보 요청
        user_response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        user_data = user_response.json()

        google_id = user_data.get('id')
        email = user_data.get('email')
        name = user_data.get('name', '')

        # 사용자 생성 또는 조회
        user, created = User.objects.get_or_create(
            social_provider='google',
            social_id=google_id,
            defaults={
                'username': f'google_{google_id}',
                'email': email,
                'first_name': name,
                'email_verified': True,
            }
        )

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })


class SocialUnlinkView(APIView):
    """소셜 계정 연동 해제"""
    permission_classes = [IsAuthenticated]

    def post(self, request, provider):
        user = request.user
        if user.social_provider != provider:
            return Response({'detail': '해당 소셜 계정과 연동되어 있지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 설정 여부 확인 (비밀번호 없으면 연동 해제 불가)
        if not user.has_usable_password():
            return Response({'detail': '소셜 연동 해제 전에 비밀번호를 설정해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        user.social_provider = ''
        user.social_id = ''
        user.save()

        return Response({'message': '소셜 계정 연동이 해제되었습니다.'})
