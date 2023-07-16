from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.views.generic.edit import FormMixin
from .forms import ProductFilterForm
from .models import Product
from .forms import ProductSearchForm, ProductAddToCartForm
from cart.views import add_to_cart


class Products(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 2
    extra_context = {"search_form": ProductSearchForm}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset())
        context["form"] = self.filter_form

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search_field")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        self.filter_form = ProductFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            categories = self.filter_form.cleaned_data.get("categories")
            min_field, max_field = self.filter_form.cleaned_data.get(
                "min_price"
            ), self.filter_form.cleaned_data.get("max_price")

            if categories:
                queryset = queryset.filter(categories__name__in=categories)
            if min_field:
                queryset = queryset.filter(price__gte=min_field)
            if max_field:
                queryset = queryset.filter(price__lte=max_field)

        return queryset


class ProductDetails(FormMixin, DetailView):
    model = Product
    template_name = "products/product.html"
    form_class = ProductAddToCartForm

    def get_success_url(self):
        return reverse("product", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        quantity = int(request.POST.get("quantity"))
        add_to_cart(request, self.object.pk, quantity)

        return self.form_valid(self.get_form())
