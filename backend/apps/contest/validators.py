import os
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['.hwp', '.pdf', '.docx', '.doc']
BLOCKED_EXTENSIONS = ['.exe', '.sh', '.bat', '.cmd', '.ps1', '.js', '.php']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_script_file(file):
    """원고 파일 검증"""
    ext = os.path.splitext(file.name)[1].lower()

    if ext in BLOCKED_EXTENSIONS:
        raise ValidationError('보안상 해당 파일 형식은 업로드할 수 없습니다.')

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'hwp, pdf, doc, docx 파일만 업로드 가능합니다. (현재: {ext})'
        )

    if file.size > MAX_FILE_SIZE:
        raise ValidationError('파일 크기는 10MB를 초과할 수 없습니다.')
