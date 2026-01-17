from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import VolunteerApplication, Donation
from .serializers import VolunteerApplicationSerializer, DonationSerializer


class VolunteerApplyView(generics.CreateAPIView):
    """자원봉사 신청 API"""
    queryset = VolunteerApplication.objects.all()
    serializer_class = VolunteerApplicationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response({
            'id': application.id,
            'message': '자원봉사 신청이 완료되었습니다.'
        }, status=status.HTTP_201_CREATED)


class DonationCreateView(generics.CreateAPIView):
    """후원 신청 API"""
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()
        return Response({
            'id': donation.id,
            'message': '후원 신청이 완료되었습니다.',
            'amount': donation.amount
        }, status=status.HTTP_201_CREATED)
