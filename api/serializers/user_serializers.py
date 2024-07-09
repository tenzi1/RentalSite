"""Serializers for User and Authentication models"""

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ChatUserDetailSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "profile_img"]

    def get_profile_img(self, object):
        if object.profile.image:
            return self.context["request"].build_absolute_uri(object.profile.image.url)
        else:
            return self.context["request"].build_absolute_uri(
                "/static/images/profile.png"
            )
