from products.models import Product
from cart.models import OrderProduct
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail


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


def is_quantity_valid(quantity, filled_quantity, product):
    # Don't check if it's pre order
    if not product.pre_order:
        if product.quantity <= 0 or product.quantity - (filled_quantity + quantity) < 0:
            return False
    return True


def empty_cart(cart, order):
    # Update products and create the order products
    products = Product.objects.all()
    for product_slug, quantity in cart.items():
        product = products.get(slug=product_slug)

        if not product.pre_order:
            product.quantity -= quantity
            product.save()

        OrderProduct.objects.create(order=order, product=product, quantity=quantity)

    cart = {}


def validate_cart(cart):
    cart_copy = cart.copy()
    is_cart_valid = cart != {}

    if is_cart_valid:
        products = Product.objects.all()
        for slug, quantity in cart.items():
            product = products.get(slug=slug)
            is_product_valid = is_quantity_valid(quantity, 0, product)

            # Remove invalid product
            if not is_product_valid:
                cart_copy.pop(slug)
                is_cart_valid = False

    # Update cart
    cart = cart_copy

    return is_cart_valid


def send_order_email(request, order):
    host_email = settings.EMAIL_HOST_USER
    order_details_url = reverse("admin:cart_order_change", args=[order.pk])
    link_url = request.build_absolute_uri(order_details_url)
    link_html = format_html('<a href="{}">Виж</a>', link_url)
    message = f"Нова поръчка е направена: {link_html}"

    try:
        send_mail(
            subject="Нова Поръчка",
            message=message,
            html_message=message,
            from_email=host_email,
            recipient_list=[host_email],
        )
    except:
        pass
