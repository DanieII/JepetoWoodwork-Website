from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from products.models import Product
from .forms import ContactForm
from django.contrib.auth.models import send_mail
from django.conf import settings


class Home(ListView):
    model = Product
    template_name = "common/home.html"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-date_added")[:5]
        return queryset


class Contacts(FormView):
    template_name = "common/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = f"from {name}({email})\n" + form.cleaned_data["message"]
        host_email = settings.EMAIL_HOST_USER

        send_mail(
            subject=subject,
            message=message,
            from_email=host_email,
            recipient_list=[host_email],
        )
        send_mail(subject, message, from_email=host_email, recipient_list=[host_email])

        return super().form_valid(form)
