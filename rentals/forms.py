"""Forms for Rental Models"""

from django import forms

from .models import Rental, Category


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
