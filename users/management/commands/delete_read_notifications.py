from django.core.management.base import BaseCommand
from django.utils import timezone
from models import Notification 

class Command(BaseCommand):
    help = '읽은 알림을 자정에 삭제합니다.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        read_notifications = Notification.objects.filter(is_read=True, timestamp__lt=now)
        count = read_notifications.count()
        read_notifications.delete()
        self.stdout.write(self.style.SUCCESS(f'{count}개의 읽은 알림이 삭제되었습니다.'))
