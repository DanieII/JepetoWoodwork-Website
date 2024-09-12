from django.contrib import admin
from .models import Order
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "contact",
        "city",
        "address",
        "apartment_building",
        "postal_code",
        "delivery_type",
        "notes",
        "products",
        "total",
        "created_on",
        "number",
    ]
    search_fields = ["first_name", "number"]
    search_help_text = "First Name or Order Number"
    list_filter = ["delivery_type"]

    @staticmethod
    def full_name(order):
        return order.first_name + " " + order.last_name

    @staticmethod
    def contact(order):
        return order.email + "/" + str(order.phone_number)

    @staticmethod
    def products(order):
        result = []
        for product in order.orderproduct_set.all():
            product_url = reverse(
                "product_details", kwargs={"slug": product.product.slug}
            )
            product_link = f'<a href="{product_url}">{product.product.name}</a>'
            result.append(
                f"{product.quantity} {product_link} за {product.product_total} лв."
            )

        return mark_safe(", ".join(result))

    @staticmethod
    def total(order):
        return f"{order.total_price} лв."
