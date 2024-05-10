from django.urls import path

from .views import SignupPageView, update_profile, confirm_logout

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("profile/", update_profile, name="profile"),
    path("confirm_logout/", confirm_logout, name="confirm-logout"),
]
