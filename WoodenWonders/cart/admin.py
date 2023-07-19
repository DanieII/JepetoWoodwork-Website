from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["full_name", "contact", "city", "address", "products", "total"]

    @staticmethod
    def full_name(order):
        return order.first_name + " " + order.last_name

    @staticmethod
    def contact(order):
        user = order.user
        return user.email or user.phone_number

    @staticmethod
    def products(order):
        result = []
        for product in order.orderproduct_set.all():
            result.append(
                f"{product.quantity} {product.product.name} for ${product.product_total}"
            )

        return ", ".join(result)

    @staticmethod
    def total(order):
        return "$" + str(
            sum(
                float(product.product_total) for product in order.orderproduct_set.all()
            )
        )
