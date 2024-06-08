from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CreateRentalForm, CreateRentalImageForm, UpdateRentalForm
from .models import Rental, RentalImage, RentalLocation

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class RentalDetailView(generic.DetailView):
    model = Rental
    template_name = "rental_detail.html"
    pk_url_kwarg = "rental_id"

    def get_queryset(self):
        return (
            self.model.objects.select_related("owner", "category", "location")
            .prefetch_related("rental_images")
            .only(
                "owner__first_name",
                "owner__last_name",
                "category__name",
                "location",
                "title",
                "description",
                "num_bedrooms",
                "num_bathrooms",
                "is_bathroom_shared",
                "has_attached_bathroom",
                "is_kitchen_shared",
                "square_footage",
                "monthly_rent",
                "available_for_rent",
                "date_added",
                "is_featured",
            )
        )


class CreateRentalView(LoginRequiredMixin, generic.CreateView):
    """Returns form to create rental instance."""

    model = Rental
    template_name = "rental_add.html"
    form_class = CreateRentalForm

    def form_valid(self, form):
        userprofile = self.request.user.profile
        form.instance.owner = userprofile

        latitude = form.cleaned_data.get("latitude", None)
        longitude = form.cleaned_data.get("longitude", None)
        address = form.cleaned_data.get("address", "Unknown")
        rental_location, created = RentalLocation.objects.get_or_create(
            latitude=latitude, longitude=longitude, address=address
        )
        form.instance.location = rental_location

        rental = form.save()
        return HttpResponseRedirect(reverse("upload-rental-image", args=[rental.id]))


class UpdateRentalView(LoginRequiredMixin, generic.UpdateView):
    """View to update particular rental instance."""

    model = Rental
    template_name = "rental_update.html"
    form_class = UpdateRentalForm
    pk_url_kwarg = "rental_id"

    def form_valid(self, form):

        latitude = form.cleaned_data.get("latitude", None)
        longitude = form.cleaned_data.get("longitude", None)
        address = form.cleaned_data.get("address", "Unknown")
        rental_location, created = RentalLocation.objects.get_or_create(
            latitude=latitude, longitude=longitude, address=address
        )
        form.instance.location = rental_location
        rental = form.save()
        return HttpResponseRedirect(reverse("rental-detail", args=[rental.id]))


def upload_rental_image(request, rental_id):
    """Upload rental images"""
    if request.method == "POST":
        form = CreateRentalImageForm(request.POST, request.FILES)
        if form.is_valid():
            rental = get_object_or_404(Rental, pk=rental_id)
            rental_images = [
                RentalImage(rental=rental, image=img)
                for img in request.FILES.getlist("image")
            ]
            RentalImage.objects.bulk_create(rental_images)
            return redirect("home")
    else:
        form = CreateRentalImageForm()

    return render(request, "rental_image_add.html", {"form": form})
