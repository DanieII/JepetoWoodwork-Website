from django.shortcuts import redirect, render
from products.models import Product
from .models import Order, OrderProduct
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django import forms


def add_to_cart(request, pk):
    cart = request.session.get("cart", {})

    if not cart.get(pk):
        cart[pk] = 0
    cart[pk] += 1

    request.session["cart"] = cart

    return redirect(request.META.get("HTTP_REFERER"))


def cart(request):
    cart_products = {
        Product.objects.get(pk=int(pk)): quantity
        for pk, quantity in request.session.get("cart", {}).items()
    }

    total_price = 0
    for product, quantity in cart_products.items():
        total_price += product.price * quantity

    context = {
        "cart_products": cart_products,
        "total_price": total_price,
    }
    return render(request, "cart/cart.html", context)


def increase_quantity(request, pk):
    request.session["cart"][pk] += 1
    request.session.save()

    return redirect(reverse("cart"))


def decrease_quantity(request, pk):
    cart = request.session["cart"]
    cart_product = cart[pk]

    if cart_product > 1:
        cart_product -= 1
        cart[pk] = cart_product
        request.session["cart"] = cart
        request.session.save()

    return redirect(reverse("cart"))


def remove_product(request, pk):
    request.session["cart"].pop(pk)
    request.session.save()

    return redirect(reverse("cart"))


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["first_name", "last_name", "city", "address"]
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("order_success")

    def get_form(self):
        form = super().get_form()

        for field_name, field in form.fields.items():
            field.widget = forms.TextInput(
                attrs={"placeholder": field_name.title().replace("_", " ")}
            )

        return form

    def get(self, request, *args, **kwargs):
        if not request.session.get("cart"):
            return redirect(reverse("products"))
        return super().get(request)

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        cart = self.request.session["cart"]
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        self.request.session["cart"] = {}

        return super().form_valid(form)


class OrderSuccessView(TemplateView):
    template_name = "cart/success.html"
