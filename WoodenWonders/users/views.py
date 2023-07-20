from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from users.forms import CustomUserForm, CustomLoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .mixins import HandleReviewMessageMixin, ProhibitLoggedUsersMixin


class UserRegisterView(HandleReviewMessageMixin, ProhibitLoggedUsersMixin, CreateView):
    form_class = CustomUserForm
    template_name = "users/base-authentication.html"
    success_url = reverse_lazy("home")
    extra_context = {"state": "Register"}

    def get_success_url(self):
        next = self.request.POST.get("next")
        return next if next else self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next")

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)

        return response


class UserLoginView(HandleReviewMessageMixin, ProhibitLoggedUsersMixin, LoginView):
    form_class = CustomLoginForm
    template_name = "users/base-authentication.html"
    extra_context = {"state": "Login"}


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/details.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
