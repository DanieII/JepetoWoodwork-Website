from django.contrib import admin

from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = ['name', 'price', 'quantity', 'all_categories']

    @staticmethod
    def all_categories(product):
        return ', '.join(p.name for p in product.categories.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
