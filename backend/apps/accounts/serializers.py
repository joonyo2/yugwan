from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """회원 정보 조회/수정용 Serializer"""
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)
    admin_level_display = serializers.CharField(source='get_admin_level_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'tier', 'tier_display', 'tier_approved_at',
            'admin_level', 'admin_level_display',
            'is_staff', 'is_superuser',
            'phone', 'address', 'birth_date', 'occupation',
            'join_source', 'join_message', 'marketing_agreed',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tier', 'tier_approved_at',
            'admin_level', 'is_staff', 'is_superuser',
            'created_at', 'updated_at'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    회원가입 Serializer
    - 모든 회원은 무료회원(FREE)으로 가입
    - tier 필드는 입력받지 않음
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'phone', 'address', 'birth_date',
            'occupation', 'join_source', 'join_message',
            'marketing_agreed'
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('이미 사용 중인 아이디입니다.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이미 등록된 이메일입니다.')
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '비밀번호가 일치하지 않습니다.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # 무료회원으로 고정
        user = User(**validated_data)
        user.tier = 'FREE'
        user.set_password(password)
        user.save()
        return user


class UserAdminSerializer(serializers.ModelSerializer):
    """관리자용 회원 정보 Serializer (모든 필드 수정 가능)"""
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)
    admin_level_display = serializers.CharField(source='get_admin_level_display', read_only=True)
    approved_by_username = serializers.CharField(source='tier_approved_by.username', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'tier', 'tier_display', 'tier_approved_at', 'approved_by_username',
            'admin_level', 'admin_level_display',
            'is_staff', 'is_superuser', 'is_active',
            'phone', 'address', 'birth_date', 'occupation',
            'join_source', 'join_message', 'marketing_agreed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
