from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ContestApplication
import requests
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ContestApplication)
def send_notification_on_status_change(sender, instance, **kwargs):
    """상태가 ACCEPTED로 변경되면 알림톡 자동 발송"""
    if instance.status == 'ACCEPTED':
        message = f"[유관순사업회] {instance.name} 학생의 웅변대회 참가가 확정되었습니다."
        send_kakao_alimtalk(instance.contact_parent, message)


def send_kakao_alimtalk(phone, message):
    """카카오 알림톡 발송"""
    api_key = settings.ALIMTALK_API_KEY
    if not api_key:
        logger.warning('ALIMTALK_API_KEY not configured')
        return None

    try:
        API_URL = 'https://kakaoapi.aligo.in/akv10/alimtalk/send/'
        payload = {
            'apikey': api_key,
            'userid': settings.ALIMTALK_USER_ID,
            'senderkey': settings.ALIMTALK_SENDER_KEY,
            'tpl_code': 'CONTEST_ACCEPTED',
            'sender': '041-564-1226',
            'receiver_1': phone,
            'subject_1': '웅변대회 참가확정',
            'message_1': message,
        }
        response = requests.post(API_URL, data=payload, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f'Alimtalk send failed: {e}')
        return None
