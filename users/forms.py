from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text="Required. Letters, digits and @/./+/-/_ only.",
        # validators=[]
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "username"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["email"].required = True
    #     self.fields["email"].unique = True
