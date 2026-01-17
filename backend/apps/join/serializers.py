from rest_framework import serializers
from .models import VolunteerApplication, Donation


class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = [
            'id', 'name', 'birth_date', 'phone', 'email', 'occupation',
            'programs', 'available_dates', 'experience', 'motivation',
            'privacy_agreed', 'is_confirmed', 'created_at'
        ]
        read_only_fields = ['id', 'is_confirmed', 'created_at']

    def validate(self, data):
        if not data.get('privacy_agreed'):
            raise serializers.ValidationError({'privacy_agreed': '개인정보 수집에 동의해주세요.'})
        return data


class DonationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_donation_type_display', read_only=True)

    class Meta:
        model = Donation
        fields = [
            'id', 'donation_type', 'type_display', 'amount',
            'donor_name', 'phone', 'email',
            'receipt_requested', 'receipt_name', 'receipt_id',
            'is_confirmed', 'confirmed_at', 'created_at'
        ]
        read_only_fields = ['id', 'is_confirmed', 'confirmed_at', 'created_at']
