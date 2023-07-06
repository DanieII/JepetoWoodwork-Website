from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'phone_number']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

    def clean(self):
        super().clean()

        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone_number'):
            raise forms.ValidationError('You must give at least one contact info (an email or a phone number)')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
