"""Url confs for rental models views."""

from django.urls import path, include
from rest_framework import routers

from api.viewsets.rental_viewsets import (
    CategoryViewSet,
    RentalViewSet,
    AddRentalView,
    AddCategoryView,
    get_rent_range,
)

# from api.viewsets.rental_viewsets import CategoryViewSet

router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"rental", RentalViewSet, basename="rental")
urlpatterns = [
    path("", include(router.urls)),
    path("add_rental/", AddRentalView.as_view(), name="add-rental"),
    path("add_category/", AddCategoryView.as_view(), name="add-category"),
    path("rent_range/", get_rent_range, name="get-rent-range"),
]
