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
        exclude = [
            "owner",
            "date_added",
            "date_modified",
            "is_deleted",
        ]


class ListRentalSerializer(serializers.ModelSerializer):
    """Serializer for listing Rental instances."""

    address = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = (
            "id",
            "title",
            "monthly_rent",
            "description",
            "address",
            "category_name",
            "images",
        )
        depth = 1

    def get_category_name(self, object):
        return object.category.name

    def get_address(self, object):
        if object.location:
            return object.location.address
        else:
            return "Unknown"

    def get_images(self, object):
        return [
            self.context["request"].build_absolute_uri(img.image_url)
            for img in object.rental_images.all()
        ]


class DetailRentalSerializer(serializers.ModelSerializer):
    """Serializer for retriving particular Rental instance."""

    class Meta:
        model = Rental
        exclude = [
            "is_deleted",
        ]
