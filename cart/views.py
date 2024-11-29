from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order
from products.models import Product
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from .helper_functions import (
    add_products_to_order,
    send_order_email,
)
from django.contrib import messages


def cart_view(request):
    cart = request.session.get("cart", {})
    cart_products = {
        Product.objects.get(slug=slug): quantity for slug, quantity in cart.items()
    }
    context = {
        "cart_products": cart_products,
        "total_price": sum(
            product.price * quantity for product, quantity in cart_products.items()
        ),
    }

    return render(request, "cart/cart.html", context)


def add_to_cart_view(request, slug, quantity=1):
    redirect_url = request.POST.get("redirect_to") or "home"
    product = Product.objects.get(slug=slug)
    cart = request.session.get("cart", {})
    cart_product_quantity = cart.get(slug, 0)

    if not product.is_available:
        messages.warning(request, f"{product.name} не е наличен продукт")
        return redirect(redirect_url)

    if not cart_product_quantity:
        cart[slug] = cart_product_quantity

    cart[slug] += quantity
    request.session["cart"] = cart

    messages.success(request, f"{product.name} е добавен в количката")

    return redirect(redirect_url)


def decrease_quantity_view(request, slug):
    product = Product.objects.get(slug=slug)
    cart = request.session.get("cart", {})
    cart_product_quantity = cart.get(slug, 0)

    if cart_product_quantity > 1:
        cart_product_quantity -= 1
        cart[slug] = cart_product_quantity
        request.session["cart"] = cart
        messages.success(request, f"{product.name} е премахнат от количката")

    return redirect(reverse("cart"))


def remove_product_view(request, slug):
    product = Product.objects.get(slug=slug)
    request.session.get("cart", {}).pop(slug)
    request.session.save()

    messages.success(request, f"{product.name} е премахнат от количката")

    return redirect(reverse("cart"))


class CheckoutView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        cart = self.request.session.get("cart", {})
        if not cart:
            return redirect("cart")

        order = form.save()
        order.save()
        add_products_to_order(cart, order)

        self.request.session["cart"] = {}

        send_order_email(self.request, order)

        messages.success(self.request, "Поръчката е изпратена")

        return super().form_valid(form)
