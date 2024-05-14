""" Viewsets for rental models."""

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from rentals.models import Category
from api.serializers.rental_serializers import CategorySerializer


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
