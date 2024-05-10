from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import CustomUserCreationForm, CreateUserProfileForm
from .models import UserProfile


class SignupPageView(generic.CreateView):
    """
    Returns User creation form. upon successfull redirects to login page.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def update_profile(request):
    """
    Return form with prepopulated user info. Used for profile information update.
    """
    if request.method == "GET":
        form = CreateUserProfileForm(instance=request.user.profile)
        return render(request, "registration/user_profile.html", {"form": form})

    elif request.method == "POST":
        form = CreateUserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("home")
        else:
            form = CreateUserProfileForm(instance=request.user.profile)
            return render(request, "registration/user_profile.html", {"form": form})


def confirm_logout(request):
    """
    Returns template with logout form.
    """
    return render(request, "account/logout.html")
