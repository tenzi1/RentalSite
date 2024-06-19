from .models import Notification


def create_rental_notification(to_user, message):
    """Creates Notification."""
    Notification.objects.create(user=to_user, message=message)
