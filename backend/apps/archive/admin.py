from django.contrib import admin
from .models import Notice, News, GalleryAlbum, GalleryImage, GalleryVideo


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'author', 'views', 'is_pinned', 'created_at']
    list_filter = ['category', 'is_pinned', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_pinned']
    ordering = ['-is_pinned', '-created_at']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'title', 'is_featured', 'published_date']
    list_filter = ['source', 'is_featured', 'published_date']
    search_fields = ['title', 'excerpt']
    list_editable = ['is_featured']
    ordering = ['-published_date']


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'event_date', 'image_count', 'is_featured', 'views']
    list_filter = ['category', 'is_featured', 'event_date']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    inlines = [GalleryImageInline]
    ordering = ['-event_date']


@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'views', 'created_at']
    search_fields = ['title']
    ordering = ['-created_at']
