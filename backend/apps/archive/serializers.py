from rest_framework import serializers
from .models import Notice, News, GalleryAlbum, GalleryImage, GalleryVideo


class NoticeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Notice
        fields = [
            'id', 'category', 'category_display', 'title', 'content',
            'author', 'views', 'is_pinned', 'created_at'
        ]


class NoticeListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Notice
        fields = [
            'id', 'category', 'category_display', 'title',
            'author', 'views', 'is_pinned', 'created_at'
        ]


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id', 'source', 'title', 'excerpt', 'link_url',
            'thumbnail', 'is_featured', 'published_date'
        ]


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption', 'order']


class GalleryAlbumSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    image_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = GalleryAlbum
        fields = [
            'id', 'category', 'category_display', 'title', 'description',
            'event_date', 'cover_image', 'is_featured', 'views', 'image_count'
        ]


class GalleryAlbumDetailSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    images = GalleryImageSerializer(many=True, read_only=True)
    image_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = GalleryAlbum
        fields = [
            'id', 'category', 'category_display', 'title', 'description',
            'event_date', 'cover_image', 'is_featured', 'views', 'image_count', 'images'
        ]


class GalleryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryVideo
        fields = ['id', 'title', 'youtube_url', 'thumbnail', 'duration', 'views', 'created_at']
