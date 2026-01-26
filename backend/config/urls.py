from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import FileResponse, Http404
import os

# 프론트엔드 정적 파일 서빙
def serve_frontend(request, path=''):
    """프론트엔드 HTML/CSS/JS 파일 서빙"""
    frontend_dir = settings.FRONTEND_DIR

    # 경로가 비어있으면 index.html
    if not path or path == '/':
        path = 'index.html'

    # 디렉토리 요청이면 index.html 추가
    full_path = os.path.join(frontend_dir, path)
    if os.path.isdir(full_path):
        path = os.path.join(path, 'index.html')
        full_path = os.path.join(frontend_dir, path)

    # .html 확장자 없이 요청된 경우 추가
    if not os.path.exists(full_path) and not path.endswith('.html'):
        html_path = full_path + '.html'
        if os.path.exists(html_path):
            full_path = html_path

    if os.path.exists(full_path) and os.path.isfile(full_path):
        # Content-Type 설정
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css; charset=utf-8',
            '.js': 'application/javascript; charset=utf-8',
            '.json': 'application/json; charset=utf-8',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2',
            '.ttf': 'font/ttf',
        }
        ext = os.path.splitext(full_path)[1].lower()
        content_type = content_types.get(ext, 'application/octet-stream')

        return FileResponse(open(full_path, 'rb'), content_type=content_type)

    raise Http404(f"File not found: {path}")


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API 엔드포인트
    path('api/v1/', include([
        path('auth/', include('apps.accounts.urls')),
        path('contest/', include('apps.contest.urls')),
        path('archive/', include('apps.archive.urls')),
        path('join/', include('apps.join.urls')),
        path('popups/', include('apps.popup.urls')),
    ])),
]

# 미디어 파일 서빙 (개발 환경)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 프론트엔드 정적 파일 서빙 (맨 마지막에 추가 - catch-all)
urlpatterns += [
    re_path(r'^(?P<path>.*)$', serve_frontend),
]
