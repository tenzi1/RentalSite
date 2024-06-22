from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification, Booking


# @receiver(post_save, sender=Booking)
# def notify_rental_owner(sender, instance, created, **kwargs):
#     print("=========================================")
#     channel_layer = get_channel_layer()
#     count = Notification.objects.filter(read=False).count()
#     async_to_sync(channel_layer.group_send)(
#         f"user_{instance.rental.owner.user.id}",
#         {"type": "send_notification", "count": count},
#     )
