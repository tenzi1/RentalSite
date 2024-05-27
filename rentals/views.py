from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .forms import CreateRentalForm
from .models import Rental

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class CreateRentalView(generic.CreateView):
    """Returns form to create rental instance."""

    model = Rental
    template_name = "rental_add.html"
    form_class = CreateRentalForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        userprofile = self.request.user.profile
        form.instance.owner = userprofile
        return super().form_valid(form)
