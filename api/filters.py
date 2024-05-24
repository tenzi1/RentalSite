"""Custom Filterset"""

import django_filters

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

    class Meta:
        model = Rental
        fields = ["title", "category"]
