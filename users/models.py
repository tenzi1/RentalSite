from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.utils.managers import ActiveManager

User = get_user_model()


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("normal_user", _("Normal User")),
        ("registered_user", _("Registered User")),
        ("renter", _("Renter")),
        ("owner", _("Owner")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    first_name_ne = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    last_name_ne = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="normal_user")
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    image = models.ImageField(upload_to="upload/profile/", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
