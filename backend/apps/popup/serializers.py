from rest_framework import serializers
from .models import Popup


class PopupSerializer(serializers.ModelSerializer):
    is_visible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Popup
        fields = [
            'id', 'title', 'pc_image', 'mobile_image', 'link_url',
            'start_at', 'end_at', 'is_active', 'is_visible'
        ]
