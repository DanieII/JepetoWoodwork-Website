from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from users.forms import CustomUserForm, CustomLoginForm
from django.contrib.auth.views import LoginView


class ProhibitLoggedUsers:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("products")
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(ProhibitLoggedUsers, CreateView):
    form_class = CustomUserForm
    template_name = "users/base-authentication.html"
    success_url = reverse_lazy("products")
    extra_context = {"state": "Register"}

    def get_success_url(self):
        return self.request.POST.get("next", self.success_url)


class UserLoginView(ProhibitLoggedUsers, LoginView):
    form_class = CustomLoginForm
    template_name = "users/base-authentication.html"
    success_url = reverse_lazy("products")
    extra_context = {"state": "Login"}


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/details.html"

    @property
    def user_has_permission(self):
        accessed_pk = self.kwargs.get("pk")
        return self.request.user.pk == accessed_pk

    def get(self, request, *args, **kwargs):
        if self.user_has_permission:
            return super().get(request, *args, **kwargs)
        raise Http404()
