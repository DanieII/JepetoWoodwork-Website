from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ["email", "phone_number", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Repeat Password"}
        )

    def clean(self):
        cleaned_data = super().clean()
        self.email = cleaned_data.get("email")
        self.phone_number = cleaned_data.get("phone_number")

        if not self.email and not self.phone_number:
            raise forms.ValidationError(
                "Either email or phone number must be provided."
            )

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Email or Phone Number"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    error_messages = {
        "invalid_login": "Please enter a correct email/phone number and password. Note that both fields may be case-sensitive.",
    }
