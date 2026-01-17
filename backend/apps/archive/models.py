from django.db import models


class Notice(models.Model):
    """공지사항 - 프론트엔드: archive/notice.html"""
    CATEGORY_CHOICES = [
        ('important', '중요'),
        ('event', '행사'),
        ('contest', '웅변대회'),
        ('general', '일반'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='카테고리')
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.CharField(max_length=50, verbose_name='작성부서')
    views = models.IntegerField(default=0, verbose_name='조회수')
    is_pinned = models.BooleanField(default=False, verbose_name='상단고정')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 관리'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class News(models.Model):
    """보도자료 - 프론트엔드: archive/news.html"""
    source = models.CharField(max_length=50, verbose_name='언론사')
    title = models.CharField(max_length=200, verbose_name='제목')
    excerpt = models.TextField(verbose_name='요약')
    link_url = models.URLField(verbose_name='원문링크')
    thumbnail = models.ImageField(
        upload_to='news/thumbnails/%Y/%m/',
        blank=True,
        verbose_name='썸네일'
    )
    is_featured = models.BooleanField(default=False, verbose_name='주요보도')
    published_date = models.DateField(verbose_name='보도일')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '보도자료'
        verbose_name_plural = '보도자료 관리'
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.source}] {self.title}"


class GalleryAlbum(models.Model):
    """갤러리 앨범 - 프론트엔드: archive/gallery.html"""
    CATEGORY_CHOICES = [
        ('contest', '웅변대회'),
        ('memorial', '추모행사'),
        ('education', '교육활동'),
        ('global', '국제교류'),
        ('meeting', '회의/행사'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='카테고리')
    title = models.CharField(max_length=200, verbose_name='앨범명')
    description = models.TextField(blank=True, verbose_name='설명')
    event_date = models.DateField(verbose_name='행사일')
    cover_image = models.ImageField(
        upload_to='gallery/covers/%Y/',
        blank=True,
        verbose_name='대표이미지'
    )
    is_featured = models.BooleanField(default=False, verbose_name='최신앨범표시')
    views = models.IntegerField(default=0, verbose_name='조회수')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '갤러리 앨범'
        verbose_name_plural = '갤러리 앨범 관리'
        ordering = ['-event_date']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    @property
    def image_count(self):
        return self.images.count()


class GalleryImage(models.Model):
    """갤러리 이미지"""
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/images/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True, verbose_name='설명')
    order = models.IntegerField(default=0, verbose_name='정렬순서')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '갤러리 이미지'
        verbose_name_plural = '갤러리 이미지'
        ordering = ['order', 'created_at']


class GalleryVideo(models.Model):
    """영상 갤러리"""
    title = models.CharField(max_length=200, verbose_name='제목')
    youtube_url = models.URLField(verbose_name='YouTube 링크')
    thumbnail = models.ImageField(upload_to='gallery/videos/', blank=True, verbose_name='썸네일')
    duration = models.CharField(max_length=10, verbose_name='재생시간')
    views = models.IntegerField(default=0, verbose_name='조회수')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '영상'
        verbose_name_plural = '영상 갤러리 관리'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
