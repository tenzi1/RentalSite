import json
import traceback
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Notification
from .redis_utils import get_redis_client

# initializing redis client
redis_client = get_redis_client()


def generate_group_name(senderId, receiver_id):
    sorted_ids = sorted([senderId, receiver_id])
    return f"chat_{sorted_ids[0]}_{sorted_ids[1]}"


class InitialConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        print("inside of init......")
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()

        await self.accept()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()

        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        count = await self.get_unread_notification_count()
        await self.send(text_data=json.dumps({"count": count, "type": "notification"}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        return await super().disconnect(code)

    async def send_notification(self, event):
        await self.send(
            text_data=json.dumps({"count": event["count"], "type": "notification"})
        )

    @database_sync_to_async
    def get_unread_notification_count(self):
        return Notification.objects.filter(read=False, user=self.scope["user"]).count()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()

        self.group_room_name = f"chat_user_{self.user.id}"
        await self.channel_layer.group_add(self.group_room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            receiver_id = text_data_json["receiverId"]
            timestamp = timezone.now().isoformat()

            # store messge in Redis
            redis_client.rpush(
                "chat_messages",
                json.dumps(
                    {
                        "message": message,
                        "senderId": self.user.id,
                        "receiverId": int(receiver_id),
                        "created_at": timestamp,
                    }
                ),
            )

            receiver_group = f"chat_user_{receiver_id}"
            await self.channel_layer.group_send(
                receiver_group,
                {"type": "chat_message", "message": message, "senderId": self.user.id},
            )
        except Exception as e:
            traceback.print_exc(e)

    async def chat_message(self, event):
        message = event["message"]
        senderId = event["senderId"]
        await self.send(
            text_data=json.dumps({"message": message, "senderId": senderId})
        )
