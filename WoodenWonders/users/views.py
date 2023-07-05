from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import CustomUserForm


class RegisterView(CreateView):
    form_class = CustomUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('products')
