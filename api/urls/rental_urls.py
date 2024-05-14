"""Url confs for rental models views."""

from django.urls import path, include
from rest_framework import routers

from api.viewsets.rental_viewsets import CategoryViewSet

# from api.viewsets.rental_viewsets import CategoryViewSet

router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
urlpatterns = [
    path("", include(router.urls)),
]
