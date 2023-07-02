from django.shortcuts import render
from django.views.generic import ListView

from products.forms import ProductFilterForm
from products.models import Product, Category


class Products(ListView):
    model = Product
    template_name = 'products/products.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['form'] = ProductFilterForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        categories = self.request.GET.getlist('categories')
        if categories:
            queryset = queryset.filter(categories__name__in=categories)

        return queryset
