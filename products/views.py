from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from .forms import ProductSortForm
from .models import Product, Category
from .forms import ProductAddToCartForm
from cart.views import add_to_cart_view


class BaseProductsView(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 4
    extra_context = {"sort_form": ProductSortForm}

    def filter_by_search_field(self, queryset):
        search_query = self.request.GET.get("search_field") or self.request.POST.get(
            "search_field"
        )
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_sorted_products(self, queryset):
        form = ProductSortForm((self.request.GET or self.request.POST) or None)
        if form.is_valid():
            sort_by = form.cleaned_data.get("sort")
            if sort_by == "low_to_high":
                queryset = queryset.order_by("price")
            elif sort_by == "high_to_low":
                queryset = queryset.order_by("-price")
            elif sort_by == "new_to_old":
                queryset = queryset.order_by("-date_added")
            elif sort_by == "old_to_new":
                queryset = queryset.order_by("date_added")

        return queryset

    def perform_filtering(self, queryset):
        queryset = self.get_sorted_products(queryset)
        queryset = self.filter_by_search_field(queryset)

        return queryset


class ProductsView(BaseProductsView):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.perform_filtering(queryset)

        return queryset


class ProductsCategoryView(BaseProductsView):
    def get_queryset(self):
        slug = self.kwargs.get("slug")

        products = super().get_queryset()
        products = products.filter(categories__slug=slug)

        products = self.perform_filtering(products)

        return products


class ProductDetailsView(FormMixin, DetailView):
    model = Product
    template_name = "products/product-details.html"
    form_class = ProductAddToCartForm
    fields = "__all__"

    def get_success_url(self):
        return reverse("product_details", kwargs={"slug": self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.form = self.get_form()

        if self.form.is_valid():
            quantity = int(request.POST.get("quantity"))
            add_to_cart_view(request, self.object.slug, quantity)

        return redirect(self.get_success_url())
