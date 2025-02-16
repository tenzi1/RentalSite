from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .forms import (
    CreateRentalForm,
    CreateRentalImageForm,
    UpdateRentalForm,
    BookingForm,
)
from .models import Favorite, Rental, RentalImage, RentalLocation, Booking, Notification
from .utils import create_rental_notification, send_notification_count

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            rental = self.get_object()
            favorited_by_user = self.request.user.favorite_set.filter(
                rental=rental
            ).exists()
            context["favorated_by_user"] = favorited_by_user
            context["booking"] = self.request.user.booking_set.filter(
                rental=rental
            ).first()
            context["booked_by_user"] = (
                self.request.user.booking_set.filter(rental=rental)
                .exclude(status="CANCELLED")
                .exists()
            )
        return context


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


class UpdateRentalView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """View to update particular rental instance."""

    model = Rental
    template_name = "rental_update.html"
    form_class = UpdateRentalForm
    pk_url_kwarg = "rental_id"

    def test_func(self):
        rental = self.get_object()
        return rental.owner.user == self.request.user

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


class ListRentalImageView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = RentalImage
    template_name = "rental_images.html"
    context_object_name = "rental_images"
    pk_url_kwarg = "rental_id"

    def test_func(self):
        rental_id = self.kwargs.get("rental_id")
        rental = get_object_or_404(Rental, pk=rental_id)
        return rental.owner.user == self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(rental=self.kwargs.get("rental_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rental_id"] = self.kwargs["rental_id"]
        return context


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


def delete_rental_image(request):
    """Remove rental Image."""
    if request.method == "POST":
        image_id = request.POST.get("image_id", None)
        rental_id = request.POST.get("rental_id", None)

        if not image_id or not rental_id:
            raise PermissionDenied("Invalid request")

        try:
            image = RentalImage.objects.get(pk=image_id)
        except RentalImage.DoesNotExist:
            raise PermissionDenied("Image does not exist")

        if image.rental.owner.user != request.user:
            raise PermissionDenied("You do not have permission to delete this image.")

        image.delete()

        return HttpResponseRedirect(reverse("list-rental-images", args=[rental_id]))
    else:
        raise PermissionDenied("Invalid request method.")


@login_required
def add_favorite(request, rental_id):
    """Add favorite rental"""
    rental = get_object_or_404(Rental, id=rental_id)
    instance, created = Favorite.objects.get_or_create(user=request.user, rental=rental)
    return HttpResponseRedirect(reverse("rental-detail", args=[rental_id]))


@login_required
def remove_favorite(request, rental_id):
    """Remove favorite rental"""
    rental = get_object_or_404(Rental, id=rental_id)
    Favorite.objects.filter(user=request.user, rental=rental).delete()
    return HttpResponseRedirect(reverse("rental-detail", args=[rental_id]))


@login_required
def book_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    owner = rental.owner.user
    if owner == request.user:
        raise PermissionDenied("Owner cannot be renter for own property")

    if request.method == "GET":
        form = BookingForm()
    elif request.method == "POST":
        try:
            with transaction.atomic():
                existing_booking = Booking.objects.filter(
                    rental=rental, user=request.user
                ).exists()
                if existing_booking:
                    raise PermissionDenied("You have already booked this rental.")

                form = BookingForm(data=request.POST)
                if form.is_valid():
                    booking = form.save(commit=False)
                    booking.rental = rental
                    booking.user = request.user
                    booking.status = "PENDING"
                    booking.save()

                    message = f"New Booking: {request.user} has booked your rental {rental_id}"
                    create_rental_notification(
                        to_user=owner, message=message, rental_id=rental_id
                    )
                    # send_notification_count(to_user=owner)
                else:
                    return render(request, "booking_form.html", {"form": form})

        except Exception as e:
            print("Exception raised", e)
            raise PermissionDenied(f"Failed to book rental: {str(e)}")

        return HttpResponseRedirect(reverse("home"))
    else:
        raise PermissionDenied("Invalid request method.")
    return render(request, "booking_form.html", {"form": form})


@login_required
def cancel_booking(request, rental_id):
    if request.method == "POST":
        booking = Booking.objects.filter(user=request.user, rental_id=rental_id)
        if booking.exists():
            booking = booking.first()
            booking.status = "CANCELLED"
            booking.save()

            message = f"Booking Cancelled: {request.user} has cancelled booking of rental {rental_id}"
            create_rental_notification(
                to_user=booking.rental.owner.user, message=message, rental_id=rental_id
            )
            # send_notification_count(to_user=booking.rental.owner.user)
        return HttpResponseRedirect(reverse("home"))
    raise PermissionDenied("Invalid request method.")


@login_required
def update_booking(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    owner = rental.owner.user
    if owner == request.user:
        raise PermissionDenied("Owner cannot be renter for own property")

    if request.method == "GET":
        booking = Booking.objects.filter(user=request.user, rental=rental).first()
        form = BookingForm(instance=booking)

    elif request.method == "POST":
        booking = Booking.objects.filter(user=request.user, rental=rental).first()
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = "PENDING"
            booking.save()

            message = f"Booking Updated: {request.user} has updated booking of rental {rental_id}"
            create_rental_notification(
                to_user=owner, message=message, rental_id=rental_id
            )
            # send_notification_count(to_user=owner)
            return HttpResponseRedirect(reverse("home"))
    else:
        raise PermissionDenied("Invalid request method.")
    return render(request, "booking_form.html", {"form": form})


class BookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = "booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self) -> QuerySet[reverse_lazy]:
        rental_id = self.kwargs["rental_id"]
        rental = get_object_or_404(Rental, id=rental_id)
        self.is_owner = self.request.user == rental.owner.user
        if self.is_owner:
            return self.model.objects.select_related("user", "rental").filter(
                rental=rental
            )
        return self.model.objects.select_related("user", "rental").filter(
            user=self.request.user, rental=rental
        )

    def get_context_data(self, **kwargs: reverse_lazy):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = self.is_owner
        return context


class BookingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Booking
    template_name = "booking_detail.html"
    pk_url_kwarg = "rental_id"
    context_object_name = "booking"

    def get_object(self):
        rental_id = self.kwargs.get("rental_id")
        user = self.request.user

        query = Q(rental_id=rental_id) & (Q(user=user) | Q(rental__owner__user=user))

        booking = Booking.objects.filter(query).select_related("user", "rental").first()
        if booking is None:
            raise Booking.DoesNotExist
        return booking
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except Booking.DoesNotExist:
            return render(self.request, "404.html", status=404)


@login_required
def confirm_booking(request):
    """Confirmation of booking and rejection of other bookings for a particular rental instance."""
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        if not booking_id:
            raise PermissionDenied("Booking ID is required.")

        booking = get_object_or_404(
            Booking.objects.select_related("rental"), pk=booking_id
        )
        owner = booking.rental.owner.user

        if request.user != owner:
            raise PermissionDenied("Only the owner can confirm and reject bookings.")

        try:
            with transaction.atomic():
                booking.status = "CONFIRMED"
                booking.save()

                booking.rental.available_for_rent = False
                booking.rental.save()

                confirm_message = f"Booking: {request.user} has confirmed the booking of rental {booking.rental.id}"
                create_rental_notification(
                    to_user=booking.user,
                    message=confirm_message,
                    rental_id=booking.rental.id,
                )
                # send_notification_count(to_user=booking.user)

                rejected_bookings = booking.rental.booking_set.exclude(id=booking_id)
                rejected_bookings.update(status="REJECTED")

                for rejected_booking in rejected_bookings:
                    reject_message = f"Booking: {request.user} has rejected the booking of rental {booking.rental.id}"
                    create_rental_notification(
                        to_user=rejected_booking.user,
                        message=reject_message,
                        rental_id=booking.rental_id,
                    )
                    # send_notification_count(to_user=rejected_booking.user)

        except Exception as e:
            raise PermissionDenied(f"Failed to update booking status: {str(e)}")

        return HttpResponseRedirect(reverse("bookings", args=[booking.rental_id]))

    else:
        raise PermissionDenied("Invalid request method.")


@login_required
def reject_booking(request):
    """Reject booking of a particular rental instance."""
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        if not booking_id:
            raise PermissionDenied("Booking ID is required.")

        booking = get_object_or_404(
            Booking.objects.select_related("rental"), pk=booking_id
        )
        owner = booking.rental.owner.user

        if request.user != owner:
            raise PermissionDenied("Only the owner can reject the booking.")

        try:
            with transaction.atomic():
                booking.status = "REJECTED"
                booking.save()

                # Check if no other bookings are confirmed
                if not booking.rental.booking_set.filter(status="CONFIRMED").exists():
                    booking.rental.available_for_rent = True
                    booking.rental.save()

                message = f"Booking: {request.user} has rejected the booking of rental {booking.rental.id}"
                create_rental_notification(
                    to_user=booking.user, message=message, rental_id=booking.rental.id
                )
                # send_notification_count(to_user=booking.user)

        except Exception as e:
            raise PermissionDenied(f"Failed to reject booking: {str(e)}")

        return HttpResponseRedirect(reverse("bookings", args=[booking.rental.id]))

    else:
        raise PermissionDenied("Invalid request method.")


@login_required
def remove_booking(request):
    """Remove booking of a particular rental instance."""
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        if not booking_id:
            raise PermissionDenied("Booking ID is required.")

        booking = get_object_or_404(
            Booking.objects.select_related("rental"), pk=booking_id
        )

        with transaction.atomic():
            booking.delete()

        return HttpResponseRedirect(reverse("booking-detail", args=[booking.rental.id]))

    else:
        raise PermissionDenied("Invalid request method.")


class NotificationListView(generic.ListView):
    model = Notification
    template_name = "notification_list.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[reverse_lazy]:
        return self.model.objects.order_by("-created_at")
