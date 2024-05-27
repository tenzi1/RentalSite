from django.urls import path

from .views import HomePageView, CreateRentalView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("add_rental/", CreateRentalView.as_view(), name="create-rental"),
]
