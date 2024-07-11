"""factory classes to generate dummy data for models"""

import factory
import random
from decimal import Decimal
from faker import Faker
from django.contrib.auth import get_user_model

from .models import *


User = get_user_model()

fake = Faker()


def generate_rental_title(category):
    """generate fake title for rental"""

    adjectives = ["Spacious", "Cozy", "Modern", "Luxurious", "Charming"]
    locations = [
        "in the city center",
        "with a great view",
        "near the park",
        "in a quiet neighborhood",
        "close to amenities",
    ]
    return f"{random.choice(adjectives)} {category.name} {random.choice(locations)}"


def generate_rental_description():
    sentences = [
        "This property offers a comfortable living space with modern amenities.",
        "Enjoy the serene environment and convenient location.",
        "Perfect for families and individuals looking for a cozy home.",
        "Features include a spacious kitchen, modern bathrooms, and a large living area.",
        "Located in a prime area with easy access to public transport and shopping centers.",
    ]
    return " ".join(random.sample(sentences, k=3))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda _: fake.email())
    password = factory.PostGenerationMethodCall("set_password", "password123")


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda obj: obj.user.first_name)
    last_name = factory.LazyAttribute(lambda obj: obj.user.last_name)
    email = factory.LazyAttribute(lambda obj: obj.user.email)
    phone = factory.Faker("phone_number")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Iterator(
        [
            "Studio",
            "Apartment",
            "House",
            "Condo",
            "Townhouse",
            "Villa",
            "Cabin",
            "Loft",
            "Duplex",
            "Penthouse",
        ]
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return model_class.objects.get_or_create(**kwargs)[0]


class RentalLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RentalLocation

    address = factory.LazyAttribute(lambda _: fake.address())
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())


class RentalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rental

    category = factory.SubFactory(CategoryFactory)
    location = factory.SubFactory(RentalLocationFactory)
    title = factory.LazyAttribute(lambda obj: generate_rental_title(obj.category))
    description = factory.LazyAttribute(lambda _: generate_rental_description())
    monthly_rent = factory.LazyAttribute(
        lambda _: Decimal(random.uniform(5000, 100000))
    )
    num_bedrooms = factory.LazyAttribute(lambda _: fake.random_digit())
    num_bathrooms = factory.LazyAttribute(lambda _: fake.random_digit())
    has_attached_bathroom = factory.LazyAttribute(lambda _: fake.boolean())
    is_kitchen_shared = factory.LazyAttribute(lambda _: fake.boolean())
    square_footage = factory.LazyAttribute(lambda _: fake.random_number(digits=2))
    available_for_rent = factory.LazyAttribute(lambda _: fake.boolean())
    date_added = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    date_modified = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    is_featured = factory.LazyAttribute(lambda _: fake.boolean())

    @factory.lazy_attribute
    def owner(self):
        return UserProfile.objects.order_by("?").first()
