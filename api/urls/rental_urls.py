"""Url confs for rental models views."""

from django.urls import path, include
from rest_framework import routers

from api.viewsets.rental_viewsets import (
    CategoryViewSet,
    ChatViewSet,
    RentalViewSet,
    AddRentalView,
    AddCategoryView,
    NotificationViewSet,
    get_rent_range,
    get_latest_chat_for_user,
)

router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"chats", ChatViewSet, basename="chats")
router.register(r"rental", RentalViewSet, basename="rental")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
    path("add_rental/", AddRentalView.as_view(), name="add-rental"),
    path("add_category/", AddCategoryView.as_view(), name="add-category"),
    path("rent_range/", get_rent_range, name="get-rent-range"),
    path("latest_chats/", get_latest_chat_for_user, name="get-latest-chats"),
]
