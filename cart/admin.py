from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ["product", "quantity", "total"]
    verbose_name = "Поръчан продукт"
    verbose_name_plural = "Поръчани продукти"

    @staticmethod
    def total(order_product):
        return f"{order_product.total_price} лв."


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "total_price_text",
        "created_on",
        "number",
    ]
    search_fields = ["number"]
    search_help_text = "Търсене по номер на поръчка"
    fieldsets = [
        (
            "Лична информация",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                ]
            },
        ),
        (
            "Адрес за доставка",
            {
                "fields": [
                    "city",
                    "address",
                ]
            },
        ),
        (
            "Детайли за поръчката",
            {
                "fields": [
                    "total_price_text",
                    "number",
                    "created_on",
                ]
            },
        ),
    ]
    inlines = [OrderProductInline]

    def has_change_permission(self, request, obj=None):
        return False

    @staticmethod
    @admin.display(description="Обща цена")
    def total_price_text(order):
        return f"{order.total_price} лв."
