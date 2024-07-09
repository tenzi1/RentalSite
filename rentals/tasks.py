import json
from celery import shared_task
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Chat
from .redis_utils import get_redis_client

redis_client = get_redis_client()

User = get_user_model()


@shared_task
def test_task(arg1, arg2):
    result = arg1 + arg2
    return result


@shared_task
def save_messages_from_redis():
    messages_data = []

    while True:
        message_data = redis_client.lpop("chat_messages")
        if not message_data:
            break
        messages_data.append(json.loads(message_data))

    if messages_data:
        user_ids = set()
        for message in messages_data:
            user_ids.add(message["senderId"])
            user_ids.add(message["receiverId"])

        print("user_ids===>", user_ids)
        print("user==============", User)
        print("type", type(User))

        users = User.objects.filter(id__in=user_ids)
        user_map = {user.id: user for user in users}

        messages = []
        for message_data in messages_data:
            sender = user_map[message_data["senderId"]]
            receiver = user_map[message_data["receiverId"]]
            messages.append(
                Chat(
                    message=message_data["message"],
                    receiver=receiver,
                    sender=sender,
                    created_at=message_data["created_at"],
                )
            )
        Chat.objects.bulk_create(messages)
