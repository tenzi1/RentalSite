"""Forms for Rental Models"""

from django import forms

from .models import Rental, Category, RentalImage


class CreateRentalForm(forms.ModelForm):

    CHOICES = [
        (True, "Yes"),
        (False, "No"),
    ]
    title = forms.CharField(required=True, help_text="Short Title for rental")
    num_bedrooms = forms.IntegerField(label="Number of Rooms", initial=0)
    num_bathrooms = forms.IntegerField(label="Number of Bathrooms", initial=0)
    is_bathroom_shared = forms.ChoiceField(
        label="Is bathroom shared?", widget=forms.RadioSelect, choices=CHOICES
    )
    has_attached_bathroom = forms.ChoiceField(
        label="Has attach bathroom?",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    is_kitchen_shared = forms.ChoiceField(
        label="Is kitchen shared?", widget=forms.RadioSelect, choices=CHOICES
    )
    monthly_rent = forms.DecimalField(help_text="Monthly rental price in NRS.")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select,
    )

    class Meta:
        model = Rental
        fields = [
            "title",
            "description",
            "num_bedrooms",
            "num_bathrooms",
            "is_bathroom_shared",
            "has_attached_bathroom",
            "is_kitchen_shared",
            "square_footage",
            "category",
            "monthly_rent",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["latitude"] = forms.DecimalField(
            required=False, widget=forms.HiddenInput()
        )
        self.fields["longitude"] = forms.DecimalField(
            required=False, widget=forms.HiddenInput()
        )
        self.fields["address"] = forms.CharField(widget=forms.HiddenInput())


class UpdateRentalForm(forms.ModelForm):

    CHOICES = [
        (True, "Yes"),
        (False, "No"),
    ]
    title = forms.CharField(required=True, help_text="Short Title for rental")
    num_bedrooms = forms.IntegerField(label="Number of Rooms", initial=0)
    num_bathrooms = forms.IntegerField(label="Number of Bathrooms", initial=0)
    is_bathroom_shared = forms.ChoiceField(
        label="Is bathroom shared?", widget=forms.RadioSelect, choices=CHOICES
    )
    has_attached_bathroom = forms.ChoiceField(
        label="Has attach bathroom?",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    is_kitchen_shared = forms.ChoiceField(
        label="Is kitchen shared?", widget=forms.RadioSelect, choices=CHOICES
    )
    monthly_rent = forms.DecimalField(help_text="Monthly rental price in NRS.")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select,
    )

    class Meta:
        model = Rental
        fields = [
            "title",
            "description",
            "num_bedrooms",
            "num_bathrooms",
            "is_bathroom_shared",
            "has_attached_bathroom",
            "is_kitchen_shared",
            "square_footage",
            "category",
            "monthly_rent",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("==========>")
        location = self.instance.location
        self.fields["latitude"] = forms.DecimalField(
            required=False,
            widget=forms.HiddenInput(),
            initial=location.latitude,
        )
        self.fields["longitude"] = forms.DecimalField(
            required=False,
            widget=forms.HiddenInput(),
            initial=location.longitude,
        )
        self.fields["address"] = forms.CharField(
            widget=forms.HiddenInput(), initial=location.address
        )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateRentalImageForm(forms.ModelForm):
    """Form for adding RentalImages"""

    # images = MultipleFileField(required=True)

    image = forms.FileField(
        widget=forms.FileInput(attrs={"name": "image", "type": "file"}),
        help_text="Add your rental image.",
    )

    class Meta:
        model = RentalImage
        fields = ["image"]


# class UploadFileForm(forms.Form):
