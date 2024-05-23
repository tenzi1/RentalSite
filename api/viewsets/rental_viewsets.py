""" Viewsets for rental models."""

from django.db import connection
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters

from api.filters import RentalFilterSet
from api.serializers.rental_serializers import (
    CategorySerializer,
    CreateRentalSerializer,
    DetailRentalSerializer,
    ListRentalSerializer,
)
from rentals.models import Category, Rental


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Rental"])
class RentalViewSet(viewsets.ModelViewSet):
    """Viewset for CRUD of Rental instance."""

    queryset = Rental.objects.all()
    serializer_class = CreateRentalSerializer
    http_method_names = ["get"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = RentalFilterSet
    search_fields = ["location__address", "title"]
    ordering_fields = ["id", "date_added"]
    ordering = ["-date_added"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListRentalSerializer
        elif self.action == "retrieve":
            return DetailRentalSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "list":
            return (
                self.queryset.select_related("category", "location")
                .prefetch_related("rental_images")
                .only(
                    "title",
                    "monthly_rent",
                    "description",
                    "category__name",
                    "location__address",
                )
            )
        return super().get_queryset()
