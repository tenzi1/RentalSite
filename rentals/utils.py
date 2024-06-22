from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification


def create_rental_notification(to_user, message):
    """Creates Notification."""
    Notification.objects.create(user=to_user, message=message)


def send_notification_count(to_user):
    """Sends count of unread notification."""
    count = Notification.objects.filter(user=to_user, read=False).count()
    group_name = f"user_{to_user.id}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name, {"type": "send_notification", "count": count}
    )
