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
        "products",
        "total",
        "created_on",
    ]
    search_fields = ["first_name", "city"]
    search_help_text = "First Name or City"
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
                f"{product.quantity} {product_link} for ${product.product_total}"
            )

        return mark_safe(", ".join(result))

    @staticmethod
    def total(order):
        return "$" + str(
            sum(
                float(product.product_total) for product in order.orderproduct_set.all()
            )
        )
