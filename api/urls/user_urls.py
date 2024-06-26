"""Url configurations for User and related models."""

from django.urls import include, path

from rest_framework import routers

from api.viewsets import user_viewsets


router = routers.DefaultRouter()
router.register(r"users", user_viewsets.UserViewSet)
router.register(r"groups", user_viewsets.GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "chat_user/<int:pk>/",
        user_viewsets.ChatUserDetailView.as_view(),
        name="chat-user-detail",
    ),
]
