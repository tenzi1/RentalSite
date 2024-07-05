from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import CustomUserCreationForm, CreateUserProfileForm
from .models import UserProfile


User = get_user_model()


class SignupPageView(generic.CreateView):
    """
    Returns User creation form. upon successfull redirects to login page.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def profile_view(request, user_id=None):
    """
    Returns user profile informations.
    """
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        profile = user.profile
    else:
        profile = request.user.profile
    return render(request, "registration/user_profile.html", {"profile": profile})


@login_required
def update_profile(request, user_id):
    """
    Return form with prepopulated user info. Used for profile information update.
    """
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        raise PermissionDenied("Only user can update their profile.")

    if request.method == "GET":
        form = CreateUserProfileForm(instance=request.user.profile)
        return render(request, "registration/profile_update.html", {"form": form})

    elif request.method == "POST":
        form = CreateUserProfileForm(
            data=request.POST, files=request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile", user.id)
        else:
            form = CreateUserProfileForm(instance=request.user.profile)
            return render(request, "registration/profile_update.html", {"form": form})


def confirm_logout(request):
    """
    Returns template with logout form.
    """
    return render(request, "account/logout.html")
