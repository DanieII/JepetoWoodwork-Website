from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order
from products.models import Product
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from .helper_functions import (
    get_cart_products,
    get_total_price,
    is_quantity_valid,
    update_products,
    send_order_email,
    validate_cart,
)
from django.contrib import messages


def cart(request):
    cart_products = get_cart_products(request.session)
    context = {
        "cart_products": cart_products,
        "total_price": get_total_price(cart_products),
    }

    return render(request, "cart/cart.html", context)


def add_to_cart(request, slug, quantity=1):
    redirect_url = request.POST.get("redirect_to") or "home"
    product = Product.objects.get(slug=slug)
    cart = request.session.get("cart", {})
    filled_quantity = cart.get(slug, 0)
    is_valid = is_quantity_valid(quantity, filled_quantity, product)

    if not is_valid:
        messages.warning(request, f"{product.name} не е наличен продукт")
        return redirect(redirect_url)

    # Create new product in cart
    if not filled_quantity:
        cart[slug] = filled_quantity

    cart[slug] += quantity

    # Update cart
    request.session["cart"] = cart

    messages.success(request, f"{product.name} е добавен в количката")

    return redirect(redirect_url)


def decrease_quantity(request, slug):
    product = Product.objects.get(slug=slug)
    cart = request.session["cart"]
    cart_product_quantity = cart[slug]

    if cart_product_quantity > 1:
        cart_product_quantity -= 1
        cart[slug] = cart_product_quantity
        request.session["cart"] = cart
        request.session.save()
        messages.success(request, f"{product.name} е премахнат от количката")

    return redirect(reverse("cart"))


def remove_product(request, slug):
    product = Product.objects.get(slug=slug)
    request.session["cart"].pop(slug)
    request.session.save()

    messages.success(request, f"{product.name} е премахнат от количката")

    return redirect(reverse("cart"))


class CheckoutView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "cart/checkout.html"
    success_url = reverse_lazy("products")

    @property
    def cart(self):
        return self.request.session.get("cart", {})

    def dispatch(self, request, *args, **kwargs):
        valid_cart = validate_cart(self.cart)

        if valid_cart:
            return super().dispatch(request)

        messages.warning(
            self.request, "Празна количка или неналични продукти. Опитайте отново."
        )

        return redirect("cart")

    def form_valid(self, form):
        if not self.cart:
            return redirect("cart")

        order = form.save()
        order.save()

        update_products(self.cart, order)

        self.request.session["cart"] = {}

        messages.success(self.request, "Поръчката е запазена")

        send_order_email(self.request, order)

        return super().form_valid(form)
