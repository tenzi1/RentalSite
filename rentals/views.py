from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from .forms import CreateRentalForm, CreateRentalImageForm
from .models import Rental, RentalImage

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class CreateRentalView(generic.CreateView):
    """Returns form to create rental instance."""

    model = Rental
    template_name = "rental_add.html"
    form_class = CreateRentalForm

    def form_valid(self, form):
        userprofile = self.request.user.profile
        form.instance.owner = userprofile
        instance = form.save()
        return HttpResponseRedirect(reverse("upload-rental-image", args=[instance.id]))


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
