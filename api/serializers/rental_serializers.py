""" Serializers for Rental Models"""

from rest_framework import serializers

from rentals.models import (
    Category,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
