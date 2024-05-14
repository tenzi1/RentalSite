""" Serializers for Rental Models"""

from rest_framework import serializers

from rentals.models import Category, Rental


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for CRUD of Category instance."""

    class Meta:
        model = Category
        fields = "__all__"


class CreateRentalSerializer(serializers.ModelSerializer):
    """Serializer for creating new Rental instace."""

    class Meta:
        model = Rental
        exclude = ["owner", "date_added", "date_modified", "is_deleted"]


class ListRentalSerializer(serializers.ModelSerializer):
    """Serializer for listing Rental instances."""

    owner = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = ("id", "title", "owner", "monthly_cost")

    def get_owner(self, object):
        return object.owner.first_name


class DetailRentalSerializer(serializers.ModelSerializer):
    """Serializer for retriving particular Rental instance."""

    class Meta:
        model = Rental
        exclude = [
            "is_deleted",
        ]
