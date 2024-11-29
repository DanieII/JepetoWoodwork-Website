from products.models import Product
from cart.models import OrderProduct
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail


def add_products_to_order(cart, order):
    product_slugs = cart.keys()
    products = Product.objects.filter(slug__in=product_slugs)
    order_products = [
        OrderProduct(order=order, product=product, quantity=cart[product.slug])
        for product in products
    ]

    OrderProduct.objects.bulk_create(order_products)


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
