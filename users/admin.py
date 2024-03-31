from django.contrib import admin
from .models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "role",
        "date_created",
        "is_deleted",
    )
