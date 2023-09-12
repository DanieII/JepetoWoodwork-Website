from django.contrib.auth.views import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from products.models import Product
from .forms import ContactForm
from django.contrib.auth.models import send_mail
from django.conf import settings
from django.contrib import messages


class HomeView(ListView):
    model = Product
    template_name = "common/home.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(special=True)
        return queryset


class ContactsView(FormView):
    template_name = "common/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = f"От {name}({email})\n" + form.cleaned_data["message"]
        host_email = settings.EMAIL_HOST_USER

        send_mail(
            subject=subject,
            message=message,
            from_email=host_email,
            recipient_list=[host_email],
        )

        messages.success(self.request, "Емейлът е изпратен!")

        return super().form_valid(form)


class AboutUsView(TemplateView):
    template_name = "common/about-us.html"


class PrivacyPolicyView(TemplateView):
    template_name = "common/privacy-policy.html"


class TermsOfUseView(TemplateView):
    template_name = "common/terms-of-use.html"


class FAQView(TemplateView):
    template_name = "common/faq.html"
