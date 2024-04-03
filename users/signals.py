# from django.core.signals import request_finished
# from django.db.models.signals import pre_save
# from django.dispatch import receiver, Signal
# from django.contrib.auth import get_user_model

# User = get_user_model()


# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print("Request Finished!")


# # request_finished.connect(my_callback)

# pizza_done = Signal()

# Signal.send(sender, **kwargs)
# Signal.send_robust(sender, **kwargs)

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            email=instance.email,
        )
