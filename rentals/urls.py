from django.urls import path

from .views import HomePageView, CreateRentalView, upload_rental_image

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_rental/", CreateRentalView.as_view(), name="create-rental"),
    path(
        "upload_rental_image/<int:rental_id>/",
        upload_rental_image,
        name="upload-rental-image",
    ),
]
