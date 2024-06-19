from django.urls import path

from .views import SignupPageView, update_profile, profile_view, confirm_logout

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("profile/<int:user_id>/", profile_view, name="profile"),
    path("update_profile/", update_profile, name="update-userprofile"),
    path("confirm_logout/", confirm_logout, name="confirm-logout"),
]
