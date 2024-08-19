import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        notification_id = data["notification_id"]
        # 서버에서 알림 읽음 처리 로직 추가 (필요시)

        # 알림을 클라이언트로 전송
        await self.send(text_data=json.dumps({
            "message": f"Notification {notification_id} received",
        }))

    async def send_notification(self, event):
        message = event["message"]

        # 알림을 클라이언트로 전송
        await self.send(text_data=json.dumps({
            "message": message,
        }))
