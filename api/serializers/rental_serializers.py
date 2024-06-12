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

    title = serializers.CharField(
        label="Rental Title",
        # help_text=("(Optional) Provide a short tags for your Rental. "),
        required=True,
        style={
            # "template_pack": "rest_framework/inline",
            "placeholder": "Job Name",
            "className": "raw",
        },
    )
    description = serializers.CharField(
        help_text="Provide a short description of your rental.",
        style={"base_template": "textarea.html", "rows": 10},
    )
    num_bedrooms = serializers.IntegerField(label="Number of Rooms", required=True)
    num_bathrooms = serializers.IntegerField(label="Number of Bathroom", required=True)

    class Meta:
        model = Rental
        fields = ["title", "description", "num_bedrooms", "num_bathrooms"]
        # exclude = [
        #     "id",
        #     "owner",
        #     "location",
        #     "date_added",
        #     "date_modified",
        #     "is_deleted",
        # ]


from datetime import datetime, timezone


class ListRentalSerializer(serializers.ModelSerializer):
    """Serializer for listing Rental instances."""

    address = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    days_since_modified = serializers.SerializerMethodField()
    status = serializers.CharField(required=False, read_only=True)

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
            "days_since_modified",
            "status",
        )
        # depth = 1

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

    def get_days_since_modified(self, object):
        if object.date_modified is not None:
            return self.get_day(object.date_modified)
        else:
            return self.get_day(object.date_added)

    def get_day(self, date):
        now = datetime.now(timezone.utc)
        delta = now - date
        return delta.days

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["status"] = instance.status if hasattr(instance, "status") else None
        return rep


class DetailRentalSerializer(serializers.ModelSerializer):
    """Serializer for retriving particular Rental instance."""

    class Meta:
        model = Rental
        exclude = [
            "is_deleted",
        ]


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
        ]
