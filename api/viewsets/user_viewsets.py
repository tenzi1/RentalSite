"""Viewsets for User and other related models"""

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets

from api.serializers.user_serializers import UserSerializer, GroupSerializer


@extend_schema(tags=["User"])
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Groups"])
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
