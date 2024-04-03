from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import CustomUserCreationForm, CreateUserProfileForm
from .models import UserProfile


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfilePageView(generic.CreateView):
    form_class = CreateUserProfileForm
    success_url = reverse_lazy("home")
    template_name = "registration/user_profile.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context


def update_profile(request):
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
