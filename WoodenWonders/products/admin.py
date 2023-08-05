from django.contrib import admin
from django.contrib.admin.options import format_html
from products.models import Product, Category, ProductReview


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "price", "quantity", "all_categories", "product_image"]
    list_filter = ["categories"]
    search_fields = ["name", "categories__name"]
    search_help_text = "Name or Category"

    @staticmethod
    def all_categories(product):
        return ", ".join(p.name for p in product.categories.all())

    @staticmethod
    def product_image(product):
        return format_html(
            f'<img src="{product.image.url}" alt="{product.name} mage" style="max-height: 100px; max-width: 100px;" />',
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductReview)
class ReviewAdmin(admin.ModelAdmin):
    pass
