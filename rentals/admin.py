from django.contrib import admin
from .models import (
    Booking,
    Category,
    Rental,
    RentalImage,
    RentalLocation,
    Province,
    District,
    Country,
    Ward,
)

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = [
        "name",
    ]


class RentalAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "monthly_rent", "available_for_rent", "date_added"]
    search_fields = ["category"]


class RentalImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "name"]


class RentalLocationAdmin(admin.ModelAdmin):
    list_display = ["id", "address"]


class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country"]
    raw_id_fields = ["country"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "province"]
    raw_id_fields = ["province"]


class WardAdmin(admin.ModelAdmin):
    list_display = ["id", "district", "ward_no"]
    raw_id_fields = ["district"]


admin.site.register(Booking)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(RentalImage, RentalImageAdmin)
admin.site.register(RentalLocation, RentalLocationAdmin)
admin.site.register(Ward, WardAdmin)
