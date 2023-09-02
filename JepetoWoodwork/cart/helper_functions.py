from products.models import Product
from django.core.exceptions import ObjectDoesNotExist


def get_cart_products(session):
    return {
        Product.objects.get(slug=slug): quantity
        for slug, quantity in session.get("cart", {}).items()
    }


def get_total_price(products):
    total_price = 0

    for product, quantity in products.items():
        total_price += product.price * quantity

    return total_price


def process_cart_quantity(product_slug, product, quantity, cart, pre_order):
    product = Product.objects.get(slug=product.slug)
    cart[product_slug] += quantity

    if not pre_order:
        product.quantity -= cart[product_slug]

        if product.quantity < 0:
            cart[product_slug] += product.quantity

    return cart


def get_user_saved_checkout_information(request):
    try:
        checkout_information = request.user.savedcheckoutinformation
        return checkout_information
    except (ObjectDoesNotExist, AttributeError):
        return None


def set_saved_checkout_information_values(saved_checkout_information, fields):
    for k, v in fields.items():
        if getattr(saved_checkout_information, k):
            setattr(saved_checkout_information, k, v)

    return saved_checkout_information
