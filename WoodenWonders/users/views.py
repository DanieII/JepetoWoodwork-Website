from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .mixins import (
    HandleAcceptAndRecoverInformationFromLoginRequiredFormMixin,
    ProhibitLoggedUsersMixin,
)
from cart.models import Order
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class UserRegisterView(
    SuccessMessageMixin,
    HandleAcceptAndRecoverInformationFromLoginRequiredFormMixin,
    ProhibitLoggedUsersMixin,
    CreateView,
):
    form_class = CustomUserCreationForm
    template_name = "users/base-authentication.html"
    success_url = reverse_lazy("home")
    extra_context = {"state": "Register"}
    success_message = "Account created"

    def get_success_url(self):
        next = self.request.POST.get("next")
        return next if next != "None" else self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next")

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        login(
            self.request, user, backend="users.authentication.PhoneAndEmailAuthBackend"
        )

        return response


class UserLoginView(
    SuccessMessageMixin,
    HandleAcceptAndRecoverInformationFromLoginRequiredFormMixin,
    ProhibitLoggedUsersMixin,
    LoginView,
):
    form_class = CustomLoginForm
    template_name = "users/base-authentication.html"
    extra_context = {"state": "Login"}

    def get_success_message(self, cleaned_data):
        return f"Logged in as {cleaned_data.get('username')}"

    def form_valid(self, form):
        login(
            self.request,
            form.get_user(),
            backend="users.authentication.PhoneAndEmailAuthBackend",
        )

        return super().form_valid(form)


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/details.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserOrders(ListView):
    model = Order
    template_name = "users/order-history.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "users/change-password.html"
    success_url = reverse_lazy("user_details")
    success_message = "Your password has been changed successfully."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["old_password"].widget.attrs.update(
            {"placeholder": "Enter your current password"}
        )
        form.fields["new_password1"].widget.attrs.update(
            {"placeholder": "Enter a new password"}
        )
        form.fields["new_password2"].widget.attrs.update(
            {"placeholder": "Confirm your new password"}
        )

        return form


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")

    return redirect("login")
