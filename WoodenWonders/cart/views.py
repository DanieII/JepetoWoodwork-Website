from django.shortcuts import redirect, render
from products.models import Product


def add_to_cart(request, pk):
    cart = request.session.get("cart", {})

    if not cart.get(pk):
        cart[pk] = 0
    cart[pk] += 1

    request.session["cart"] = cart
    print(request.session["cart"])

    return redirect(request.META.get("HTTP_REFERER"))
