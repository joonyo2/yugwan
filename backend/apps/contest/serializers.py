from rest_framework import serializers
from .models import ContestApplication


class ContestApplicationSerializer(serializers.ModelSerializer):
    division_display = serializers.CharField(source='get_division_display', read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    receipt_number = serializers.CharField(read_only=True)

    class Meta:
        model = ContestApplication
        fields = [
            'id', 'contest_year', 'name', 'birth_date', 'school_name', 'grade', 'grade_display',
            'division', 'division_display', 'speech_title',
            'parent_name', 'contact_parent', 'teacher_name', 'email', 'address',
            'script_file', 'status', 'status_display',
            'rules_agreed', 'privacy_agreed', 'news_agreed',
            'created_at', 'receipt_number'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'receipt_number']


class ContestApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestApplication
        fields = [
            'contest_year', 'name', 'birth_date', 'school_name', 'grade',
            'division', 'speech_title',
            'parent_name', 'contact_parent', 'teacher_name', 'email', 'address',
            'script_file', 'rules_agreed', 'privacy_agreed', 'news_agreed'
        ]

    def validate(self, data):
        if not data.get('rules_agreed'):
            raise serializers.ValidationError({'rules_agreed': '참가요강에 동의해주세요.'})
        if not data.get('privacy_agreed'):
            raise serializers.ValidationError({'privacy_agreed': '개인정보 수집에 동의해주세요.'})
        return data
