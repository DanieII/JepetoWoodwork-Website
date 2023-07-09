from django.views.generic import ListView
from products.models import Product


class Home(ListView):
    model = Product
    template_name = 'common/home.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_added')[:5]
        return queryset
