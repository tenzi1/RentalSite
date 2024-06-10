from django.urls import path

from .views import (
    HomePageView,
    CreateRentalView,
    UpdateRentalView,
    RentalDetailView,
    ListRentalImageView,
    upload_rental_image,
    delete_rental_image,
    add_favorite,
    remove_favorite,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path(
        "add_rental/",
        CreateRentalView.as_view(),
        name="create-rental",
    ),
    path(
        "rental_detail/<int:rental_id>/",
        RentalDetailView.as_view(),
        name="rental-detail",
    ),
    path(
        "update_rental/<int:rental_id>/",
        UpdateRentalView.as_view(),
        name="update-rental",
    ),
    path(
        "upload_rental_image/<int:rental_id>/",
        upload_rental_image,
        name="upload-rental-image",
    ),
    path(
        "rental_images/<int:rental_id>/",
        ListRentalImageView.as_view(),
        name="list-rental-images",
    ),
    path(
        "remove_rental_images/",
        delete_rental_image,
        name="remove-rental-images",
    ),
    path(
        "add_favorite/<int:rental_id>",
        add_favorite,
        name="add-favorite",
    ),
    path(
        "remove_favorite/<int:rental_id>/",
        remove_favorite,
        name="remove-favorite",
    ),
]
