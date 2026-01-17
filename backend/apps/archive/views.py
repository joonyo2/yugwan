from rest_framework import generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Notice, News, GalleryAlbum, GalleryVideo
from .serializers import (
    NoticeSerializer, NoticeListSerializer, NewsSerializer,
    GalleryAlbumSerializer, GalleryAlbumDetailSerializer, GalleryVideoSerializer
)


class NoticeListView(generics.ListAPIView):
    """공지사항 목록"""
    queryset = Notice.objects.all()
    serializer_class = NoticeListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'is_pinned']
    search_fields = ['title', 'content']


class NoticeDetailView(generics.RetrieveAPIView):
    """공지사항 상세"""
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class NewsListView(generics.ListAPIView):
    """보도자료 목록"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_featured', 'source']
    search_fields = ['title', 'excerpt']

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(published_date__year=year)
        return queryset


class GalleryAlbumListView(generics.ListAPIView):
    """갤러리 앨범 목록"""
    queryset = GalleryAlbum.objects.all()
    serializer_class = GalleryAlbumSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_featured']


class GalleryAlbumDetailView(generics.RetrieveAPIView):
    """갤러리 앨범 상세 (이미지 포함)"""
    queryset = GalleryAlbum.objects.prefetch_related('images')
    serializer_class = GalleryAlbumDetailSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class GalleryVideoListView(generics.ListAPIView):
    """영상 목록"""
    queryset = GalleryVideo.objects.all()
    serializer_class = GalleryVideoSerializer
    permission_classes = [AllowAny]
