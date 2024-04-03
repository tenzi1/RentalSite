from django.urls import path

from .views import SignupPageView, update_profile, ProfilePageView

urlpatterns = [
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("profile/", update_profile, name="profile"),
    # path("profile/", ProfilePageView.as_view(), name="profile"),
    # path("profile/<int:user_id>/", ProfilePageView.as_view(), name="profile"),
]
