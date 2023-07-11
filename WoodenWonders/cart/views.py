from django.shortcuts import redirect, render
from products.models import Product


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
        for pk, quantity in request.session.get("cart").items()
    }
    context = {"cart_products": cart_products}

    return render(request, "cart/cart.html", context)
