from django.urls import path
from .views import (
    NoticeListView, NoticeDetailView, NewsListView,
    GalleryAlbumListView, GalleryAlbumDetailView, GalleryVideoListView
)

urlpatterns = [
    path('notices/', NoticeListView.as_view(), name='notice-list'),
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('gallery/albums/', GalleryAlbumListView.as_view(), name='gallery-album-list'),
    path('gallery/albums/<int:pk>/', GalleryAlbumDetailView.as_view(), name='gallery-album-detail'),
    path('gallery/videos/', GalleryVideoListView.as_view(), name='gallery-video-list'),
]
