from django.urls import path

from .views import (
    HomePageView,
    CreateRentalView,
    UpdateRentalView,
    RentalDetailView,
    ListRentalImageView,
    BookingListView,
    BookingDetailView,
    NotificationListView,
    upload_rental_image,
    delete_rental_image,
    add_favorite,
    remove_favorite,
    book_rental,
    cancel_booking,
    update_booking,
    confirm_booking,
    reject_booking,
    remove_booking,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_rental/", CreateRentalView.as_view(), name="create-rental"),
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
    path("remove_rental_images/", delete_rental_image, name="remove-rental-images"),
    path("add_favorite/<int:rental_id>", add_favorite, name="add-favorite"),
    path("remove_favorite/<int:rental_id>/", remove_favorite, name="remove-favorite"),
    path("book_rental/<int:rental_id>/", book_rental, name="book-rental"),
    path("cancel_booking/<int:rental_id>/", cancel_booking, name="cancel-booking"),
    path("update_booking/<int:rental_id>/", update_booking, name="update-booking"),
    path("bookings/<int:rental_id>/", BookingListView.as_view(), name="bookings"),
    path(
        "booking/<int:rental_id>/", BookingDetailView.as_view(), name="booking-detail"
    ),
    path("confirm_booking/", confirm_booking, name="confirm-booking"),
    path("reject_booking/", reject_booking, name="reject-booking"),
    path("remove_booking/", remove_booking, name="remove-booking"),
    path(
        "all_notifications/", NotificationListView.as_view(), name="notification-list"
    ),
]
