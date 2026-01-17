from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Popup
from .serializers import PopupSerializer


class ActivePopupListView(generics.ListAPIView):
    """현재 활성화된 팝업 목록"""
    serializer_class = PopupSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        now = timezone.now()
        return Popup.objects.filter(
            is_active=True,
            start_at__lte=now,
            end_at__gte=now
        )
