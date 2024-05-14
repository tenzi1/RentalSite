""" Viewsets for rental models."""

from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rentals.models import Category, Rental
from api.serializers.rental_serializers import (
    CategorySerializer,
    CreateRentalSerializer,
    DetailRentalSerializer,
    ListRentalSerializer,
)


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Rental"])
class RentalViewSet(viewsets.ModelViewSet):
    """Viewset for CRUD of Rental instance."""

    queryset = Rental.objects.all()
    serializer_class = CreateRentalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_featured"]
    search_fields = ["title", "owner__first_name"]
    ordering_fields = ["id", "date_added"]
    ordering = ["-date_added"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListRentalSerializer
        elif self.action == "retrieve":
            return DetailRentalSerializer
        return super().get_serializer_class()
