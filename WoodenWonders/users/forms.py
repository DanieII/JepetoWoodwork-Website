from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ["email", "phone_number", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Имейл"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Телефонен номер"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "Парола"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Повторете паролата"}
        )

    def clean(self):
        cleaned_data = super().clean()
        self.email = cleaned_data.get("email")
        self.phone_number = cleaned_data.get("phone_number")

        if not self.email and not self.phone_number:
            raise forms.ValidationError(
                "Трябва да бъде въведен поне един имейл или телефонен номер."
            )

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имейл или телефонен номер"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Парола"})
    )

    error_messages = {
        "invalid_login": "Моля въведете правилен имейл/телефонен номер и парола.",
    }
