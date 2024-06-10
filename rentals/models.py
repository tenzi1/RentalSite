from django.db import models
from django.conf import settings

# from django.contrib.gis.db import models as geo_models
from core.utils.managers import ActiveManager
from users.models import UserProfile

# Create your models here.


class IsDeleted(models.Model):
    """
    Used for archiving of objects.
    """

    is_deleted = models.BooleanField(default=False)
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True


class Category(IsDeleted):
    """
    Used for storing categories of rental properties.
    """

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class FederalModel(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    # boundary = geo_models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(FederalModel):
    class Meta:
        verbose_name_plural = "Countries"


class Province(FederalModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class District(FederalModel):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)


class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    ward_no = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Ward No. {self.ward_no}"


class RentalLocation(models.Model):
    """
    Used for storing information about Rental property location address
    """

    address = models.CharField("Address of rental property", max_length=200)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.address


def get_default_category():
    """Return Category `Studio`"""

    default_category, _ = Category.objects.get_or_create(name="Studio")
    if not default_category:
        raise Exception("Default category not found")
    return default_category


class Rental(IsDeleted):
    """
    Used for storing rental property informations.
    """

    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="rentals"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=get_default_category,
        related_name="rentals",
    )
    location = models.ForeignKey(
        RentalLocation,
        on_delete=models.SET_NULL,
        related_name="rentals",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField("Description of Rental Property")
    num_bedrooms = models.IntegerField(default=0)
    num_bathrooms = models.IntegerField(default=0)
    is_bathroom_shared = models.BooleanField(
        default=False,
        help_text="Denotes whether bathroom is personal or shared with other renter.",
    )
    has_attached_bathroom = models.BooleanField(
        default=False, help_text="Denotes whether bathroom is attached."
    )
    is_kitchen_shared = models.BooleanField(
        default=False,
        help_text="Denotes wheter the kitchen space is shared among other renters or not.",
    )
    square_footage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Overall dimension of property.",
    )
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    available_for_rent = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    rent_start_date = models.DateField(
        help_text="Rent Start Date", null=True, blank=True
    )
    rent_end_date = models.DateField(help_text="Rent End Date", null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class RentalImage(models.Model):
    rental = models.ForeignKey(
        Rental, on_delete=models.CASCADE, related_name="rental_images"
    )
    image = models.ImageField(upload_to="upload/rental/")
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        return " "

    @property
    def image_url(self):
        return f"{self.image.url}"


class Favorite(models.Model):
    """To implement favorite feature."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
