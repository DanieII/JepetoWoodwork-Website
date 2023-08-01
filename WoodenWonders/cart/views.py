from django.shortcuts import redirect, render
from products.models import Product
from .models import Order, OrderProduct
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django import forms
from common.mixins import OptionalFormFieldsMixin
from .helper_functions import get_cart_products, get_total_price, process_cart_quantity


def add_to_cart(request, slug, quantity=1):
    cart = request.session.get("cart", {})
    product = Product.objects.get(slug=slug)
    url = request.META.get("HTTP_REFERER")

    if product.quantity <= 0:
        return redirect(url)

    if not cart.get(slug):
        cart[slug] = 0

    request.session["cart"] = process_cart_quantity(slug, product, quantity, cart)

    return redirect(url)


def cart(request):
    cart_products = get_cart_products(request.session)

    context = {
        "cart_products": cart_products,
        "total_price": get_total_price(cart_products),
    }
    return render(request, "cart/cart.html", context)


def decrease_quantity(request, slug):
    cart = request.session["cart"]
    cart_product_quantity = cart[slug]

    if cart_product_quantity > 1:
        cart_product_quantity -= 1
        cart[slug] = cart_product_quantity
        request.session["cart"] = cart
        request.session.save()

    return redirect(reverse("cart"))


def remove_product(request, slug):
    request.session["cart"].pop(slug)
    request.session.save()

    return redirect(reverse("cart"))


class CheckoutView(OptionalFormFieldsMixin, LoginRequiredMixin, CreateView):
    model = Order
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "city",
        "address",
        "apartment_building",
        "postal_code",
    ]
    optional_fields = ["apartment_building"]
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("order_success")

    @property
    def user_has_products(self):
        return self.request.session.get("cart")

    def get_form(self):
        form = super().get_form()

        if self.request.user.email:
            form.fields["email"].initial = self.request.user.email
        if self.request.user.phone_number:
            form.fields["phone_number"].initial = self.request.user.phone_number

        for field_name, field in form.fields.items():
            placeholder = field.widget.attrs.get("placeholder")
            field.widget = forms.TextInput(
                attrs={"placeholder": field_name.title().replace("_", " ")}
            )

            if placeholder:
                field.widget.attrs["placeholder"] += placeholder

        return form

    def get(self, request, *args, **kwargs):
        if self.user_has_products:
            return super().get(request)
        return redirect("products")

    def get_context_data(self):
        context = super().get_context_data()
        cart_products = get_cart_products(self.request.session)
        total_price = get_total_price(cart_products)

        context["cart_products"] = cart_products
        context["total_price"] = total_price

        return context

    def form_valid(self, form):
        if not self.user_has_products:
            return redirect("products")

        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        cart = self.request.session["cart"]
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            product.quantity -= quantity
            product.save()
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        self.request.session["cart"] = {}

        return super().form_valid(form)


class OrderSuccessView(TemplateView):
    template_name = "cart/success.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.META.get("HTTP_REFERER"):
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
