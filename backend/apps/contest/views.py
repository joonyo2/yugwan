from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ContestApplication
from .serializers import ContestApplicationSerializer, ContestApplicationCreateSerializer


class ContestApplyView(generics.CreateAPIView):
    """웅변대회 참가 신청 API"""
    queryset = ContestApplication.objects.all()
    serializer_class = ContestApplicationCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response({
            'id': application.id,
            'message': '접수가 완료되었습니다.',
            'receipt_number': application.receipt_number
        }, status=status.HTTP_201_CREATED)


class MyApplicationView(generics.RetrieveAPIView):
    """내 신청 조회 API (이메일 + 연락처로 조회)"""
    serializer_class = ContestApplicationSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        phone = request.query_params.get('phone')

        if not email or not phone:
            return Response(
                {'error': '이메일과 연락처를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application = ContestApplication.objects.filter(
            email=email,
            contact_parent=phone.replace('-', '')
        ).order_by('-created_at').first()

        if not application:
            return Response(
                {'error': '신청 내역을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(application)
        return Response(serializer.data)
