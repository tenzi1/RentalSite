"""Custom Filterset"""

import django_filters
from django.db.models import F

from rentals.models import Rental


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class RentalFilterSet(django_filters.FilterSet):
    "Filter for Rental Model."
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    min_rent = django_filters.NumberFilter(field_name="monthly_rent", lookup_expr="gte")
    max_rent = django_filters.NumberFilter(field_name="monthly_rent", lookup_expr="lte")
    category = NumberInFilter(field_name="category_id", lookup_expr="in")
    address = django_filters.CharFilter(
        field_name="location__address", lookup_expr="icontains"
    )
    featured = django_filters.BooleanFilter(
        field_name="is_featured", lookup_expr="exact"
    )
    owned = django_filters.BooleanFilter(method="filter_owned_by_user")
    favorite = django_filters.BooleanFilter(method="filter_favorated_by_user")
    booking = django_filters.BooleanFilter(method="filter_booked_rentals")

    def filter_owned_by_user(self, queryset, name, value):
        """filters queryset by current owner."""
        return queryset.filter(owner__user=self.request.user).distinct()

    def filter_favorated_by_user(self, queryset, name, value):
        """filters queryset favorated by current user."""
        return queryset.filter(favorite__user=self.request.user)

    def filter_booked_rentals(self, queryset, name, value):
        """filters booked rental queryset."""
        qs = queryset.filter(booking__user=self.request.user).annotate(
            status=F("booking__status")
        )
        return qs

    class Meta:
        model = Rental
        fields = ["title", "category"]
