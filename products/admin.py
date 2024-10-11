from django.contrib import admin
from products.models import Product, Category
from .models import ProductImage
from django.utils.safestring import mark_safe


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ["product_image"]
    extra = 1
    min_num = 1

    @staticmethod
    def product_image(product_image_obj):
        return mark_safe(
            f'<img src="{product_image_obj.image.url}" style="width: 100px; height:100px;" />'
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "thumbnail_image",
        "price",
        "quantity",
        "product_categories",
    ]
    inlines = [ProductImageInline]
    list_filter = ["categories"]
    search_fields = ["name"]
    search_help_text = "Търсене по име"

    @staticmethod
    def product_categories(product):
        return ", ".join(p.name for p in product.categories.all())

    @staticmethod
    def thumbnail_image(product):
        return mark_safe(
            f'<img src="{product.thumbnail_image_url}" style="height: 100px; width: 100px;" />'
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
