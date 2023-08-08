from django.contrib import admin
from products.models import Product, Category, ProductReview
from .models import ProductImage
from django.utils.safestring import mark_safe


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ["product_image"]

    @staticmethod
    def product_image(product_image_obj):
        return mark_safe(
            f'<img src="{product_image_obj.image.url}" alt="{product_image_obj.product.name} mage" style="max-height: 100px; max-width: 100px;" />',
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    list_display = ["name", "price", "quantity", "all_categories"]
    list_filter = ["categories"]
    search_fields = ["name", "categories__name"]
    search_help_text = "Name or Category"

    @staticmethod
    def all_categories(product):
        return ", ".join(p.name for p in product.categories.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReview)
class ReviewAdmin(admin.ModelAdmin):
    pass
