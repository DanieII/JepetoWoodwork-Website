from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from .models import Product


def get_products_with_quantities(cart):
    products = Product.objects.filter(slug__in=cart.keys())
    products_with_quantities = {product: cart[product.slug] for product in products}

    return products_with_quantities


def send_email_to_admin(request, order):
    host_email = settings.DEFAULT_FROM_EMAIL
    order_details_url = reverse("admin:cart_order_change", args=[order.pk])
    order_details_absolute_uri = request.build_absolute_uri(order_details_url)

    send_mail(
        subject="Нова поръчка от Rocco Woodwork",
        message=f"Детайли за поръчка: {order_details_absolute_uri}\nНомер на поръчка: {order.number}",
        from_email=host_email,
        recipient_list=[host_email],
    )
