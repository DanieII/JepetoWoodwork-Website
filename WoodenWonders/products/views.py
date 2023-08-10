from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.views.generic.edit import FormMixin
from .forms import ProductFilterForm, ProductReview, ProductReviewForm
from .models import Product
from .forms import ProductSearchForm, ProductAddToCartForm
from cart.views import add_to_cart
from users.mixins import HandleSendAndRetrieveLoginRequiredFormInformationMixin
from .helper_functions import get_last_viewed_products


class Products(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 10
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


class ProductDetails(
    HandleSendAndRetrieveLoginRequiredFormInformationMixin, FormMixin, DetailView
):
    model = Product
    template_name = "products/product-details.html"
    form_class = ProductAddToCartForm
    mixin_form = ProductReviewForm
    fields = "__all__"
    success_message = "Review successfully added"
    MAX_LAST_VIEWED_PRODUCTS_LENGTH = 3

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        last_viewed = self.request.session.get("last_viewed", [])

        if len(last_viewed) >= self.MAX_LAST_VIEWED_PRODUCTS_LENGTH:
            last_viewed.pop(0)

        if product.slug not in last_viewed:
            last_viewed.append(product.slug)

        self.request.session["last_viewed"] = last_viewed

        return product

    def get_additional_fields(self):
        return {"user": self.request.user, "product": self.object}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["last_viewed"] = get_last_viewed_products(self.request.session)

        return context

    def get_success_url(self):
        return reverse("product_details", kwargs={"slug": self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.form = self.get_form()

        response = super().post(request)

        if self.form.is_valid():
            quantity = int(request.POST.get("quantity"))
            add_to_cart(request, self.object.slug, quantity)

        return response
