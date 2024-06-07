""" Viewsets for rental models."""

from django.db import connection
from django.db.models import Q, Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from api.filters import RentalFilterSet
from api.serializers.rental_serializers import (
    CategorySerializer,
    CreateRentalSerializer,
    DetailRentalSerializer,
    ListRentalSerializer,
    CreateCategorySerializer,
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
    ordering_fields = ["id", "date_added", "monthly_rent"]
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
                    "date_modified",
                    "date_added",
                )
            )
        return super().get_queryset()


@extend_schema(tags=["Rental"])
@api_view(["GET"])
def get_rent_range(request):
    """Returns lower and higher end of monthly rent"""
    rent = Rental.objects.aggregate(
        min_rent=Min("monthly_rent"), max_rent=Max("monthly_rent")
    )

    return Response(rent)


@extend_schema(tags=["Rental"])
class AddRentalView(APIView):
    """Add Rental View for HTML UI."""

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CreateRentalSerializer
    template_name = "rental_add.html"

    def get(self, request):
        serialzer = self.serializer_class(context={"request": request})
        return Response(data={"form": serialzer}, template_name=self.template_name)


@extend_schema(tags=["Category"])
class AddCategoryView(APIView):
    """Add Category View for HTML UI."""

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CreateCategorySerializer
    template_name = "rental_add.html"

    def get(self, request):
        serializer = self.serializer_class(context={"request": request})
        return Response(data={"form": serializer}, template_name=self.template_name)

    def post(self, request):
        print("hererere")
        data = request.POST
        print("================================================")
        print(data)
        return Response(data={"data": data}, template_name=self.template_name)
