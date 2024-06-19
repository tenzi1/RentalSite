from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification, Booking


# @receiver(post_save, sender=Notification)
# def notification_created(sender, instance, created, **kwargs):
#     # if created:
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "rental", {"type": "send_notification", "message": instance.message}
#     )


@receiver(post_save, sender=Booking)
def notify_rental_owner(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{instance.rental.owner.user.id}",
        {"type": "send_notification", "message": 1},
    )
