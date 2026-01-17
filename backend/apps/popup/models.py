from django.db import models
from django.utils import timezone


class Popup(models.Model):
    """팝업 관리 - 프론트엔드: index.html (메인페이지)"""
    title = models.CharField(max_length=100, verbose_name='제목')
    pc_image = models.ImageField(upload_to='popup/', verbose_name='PC 이미지')
    mobile_image = models.ImageField(upload_to='popup/', verbose_name='모바일 이미지')
    link_url = models.URLField(blank=True, verbose_name='클릭시 이동URL')
    start_at = models.DateTimeField(verbose_name='노출 시작일시')
    end_at = models.DateTimeField(verbose_name='노출 종료일시')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '팝업'
        verbose_name_plural = '팝업 관리'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_visible(self):
        """현재 노출 중인지 확인"""
        now = timezone.now()
        return self.is_active and self.start_at <= now <= self.end_at
