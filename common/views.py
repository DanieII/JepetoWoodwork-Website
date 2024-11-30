from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from products.models import Product
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


class HomeView(ListView):
    model = Product
    template_name = "common/home.html"


class ContactsView(FormView):
    template_name = "common/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        user_email, user_message = (
            form.cleaned_data["email"],
            form.cleaned_data["message"],
        )
        host_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject="Контактна форма от Rocco Woodwork",
            message=f"Имейл: {user_email}\nСъобщение: {user_message}",
            from_email=host_email,
            recipient_list=[host_email],
        )

        messages.success(self.request, "Имейлът е изпратен")

        return super().form_valid(form)


class PrivacyPolicyView(TemplateView):
    template_name = "common/privacy-policy.html"


class FAQView(TemplateView):
    template_name = "common/faq.html"
