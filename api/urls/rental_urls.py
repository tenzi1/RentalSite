"""Url confs for rental models views."""

from django.urls import path, include
from rest_framework import routers

from api.viewsets.rental_viewsets import CategoryViewSet, RentalViewSet

# from api.viewsets.rental_viewsets import CategoryViewSet

router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"rental", RentalViewSet, basename="rental")
urlpatterns = [
    path("", include(router.urls)),
]
