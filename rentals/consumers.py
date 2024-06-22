import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("--------------------------------------------------------")
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()

        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        count = await self.get_unread_notification_count()
        await self.send(text_data=json.dumps({"count": count}))
        # count = Notification.objects.count()
        # await self.send(text_data=json.dumps({"message": f"{count}"}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        return await super().disconnect(code)

    async def send_notification(self, event):
        print("&*******************************************")
        await self.send(text_data=json.dumps({"count": event["count"]}))

    @database_sync_to_async
    def get_unread_notification_count(self):
        return Notification.objects.filter(read=False, user=self.scope["user"]).count()
