from django.contrib.auth.views import login_required
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from .forms import ProductFilterForm, ProductReviewForm
from .models import Category, Product, ProductReview
from .forms import ProductSearchForm, ProductAddToCartForm
from cart.views import add_to_cart
from users.mixins import HandleSendAndRetrieveLoginRequiredFormInformationMixin
from .helper_functions import get_last_viewed_products


class BaseProductsView(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 10
    extra_context = {"search_form": ProductSearchForm}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset())
        context["form"] = self.filter_form
        context["categories"] = [category.name for category in Category.objects.all()]

        return context

    def filter_by_search_field(self, queryset):
        search_query = self.request.GET.get("search_field")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def filter_by_filter_form(self, queryset):
        self.filter_form = ProductFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            min_field, max_field = self.filter_form.cleaned_data.get(
                "min_price"
            ), self.filter_form.cleaned_data.get("max_price")

            if min_field:
                queryset = queryset.filter(price__gte=min_field)
            if max_field:
                queryset = queryset.filter(price__lte=max_field)

        return queryset

    def perform_filtering(self, queryset):
        queryset = self.filter_by_search_field(queryset)
        queryset = self.filter_by_filter_form(queryset)

        return queryset


class ProductsView(BaseProductsView):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.perform_filtering(queryset)

        return queryset


class ProductsCategoryView(BaseProductsView):
    def get_queryset(self):
        category = self.kwargs.get("category")
        queryset = Product.objects.filter(categories__name=category)
        queryset = self.perform_filtering(queryset)

        return queryset


class ProductDetailsView(
    HandleSendAndRetrieveLoginRequiredFormInformationMixin, FormMixin, DetailView
):
    model = Product
    template_name = "products/product-details.html"
    form_class = ProductAddToCartForm
    mixin_form = ProductReviewForm
    fields = "__all__"
    success_message = "Отзивът е запазен"
    MAX_LAST_VIEWED_PRODUCTS_LENGTH = 3

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        last_viewed = self.request.session.get("last_viewed", [])

        if product.slug not in last_viewed:
            last_viewed.append(product.slug)
            if len(last_viewed) > self.MAX_LAST_VIEWED_PRODUCTS_LENGTH:
                last_viewed.pop(0)
        else:
            last_viewed.pop(last_viewed.index(product.slug))
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


@login_required
def delete_review_view(request, pk):
    review = ProductReview.objects.get(pk=pk)

    if review.user == request.user:
        review.delete()

    product_slug = review.product.slug
    product_details_url = reverse("product_details", kwargs={"slug": product_slug})
    return redirect(product_details_url)
