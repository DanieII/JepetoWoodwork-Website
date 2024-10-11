from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ["product", "quantity", "total_price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "city",
        "total_price",
        "created_on",
        "number",
    ]
    search_fields = ["first_name", "number"]
    search_help_text = "Търсене по първо име или номер на поръчка"
    inlines = [OrderProductInline]

    def has_change_permission(self, request, obj=None):
        return False

    @staticmethod
    def full_name(order):
        return order.first_name + " " + order.last_name

    @staticmethod
    def total_price(order):
        return f"{order.total_price} лв."
