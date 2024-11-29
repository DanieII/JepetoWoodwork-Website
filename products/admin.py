from django.contrib import admin
from products.models import Product, Category
from .models import ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price_text"]
    list_filter = ["categories"]
    search_fields = ["name"]
    search_help_text = "Търсене по име"
    inlines = [ProductImageInline]

    @staticmethod
    @admin.display(description="Цена")
    def price_text(product):
        return f"{product.price} лв."


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
