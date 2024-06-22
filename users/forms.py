from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text="Required. Letters, digits and @/./+/-/_ only.",
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "username"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            "is_deleted",
            "user",
            "role",
        )
