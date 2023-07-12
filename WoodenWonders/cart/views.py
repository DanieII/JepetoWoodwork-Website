from django.shortcuts import redirect, render
from products.models import Product
from .models import Order
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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
    context = {"cart_products": cart_products}

    return render(request, "cart/cart.html", context)


def increase_quantity(request, pk):
    request.session["cart"][pk] += 1
    request.session.save()

    return redirect(request.META.get("HTTP_REFERER"))


def decrease_quantity(request, pk):
    cart = request.session["cart"]
    cart_product = cart[pk]

    if cart_product > 1:
        cart_product -= 1
        cart[pk] = cart_product
        request.session["cart"] = cart
        request.session.save()

    return redirect(request.META.get("HTTP_REFERER"))


def remove_product(request, pk):
    request.session["cart"].pop(pk)
    request.session.save()

    return redirect(request.META.get("HTTP_REFERER"))


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["first_name", "last_name", "city", "address"]
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("order_success")

    def get(self, request, *args, **kwargs):
        if not request.session.get("cart"):
            return redirect(request.META.get("HTTP_REFERER"))
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
