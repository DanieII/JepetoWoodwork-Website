from .models import Product, Category
from django.core.cache import cache


def get_products_queryset():
    PRODUCTS_CACHE_KEY = "products"
    PRODUCTS_TTL = 60 * 60 * 24 * 7

    products = cache.get(PRODUCTS_CACHE_KEY)

    if products is None:
        products = Product.objects.all()
        cache.set(PRODUCTS_CACHE_KEY, products, PRODUCTS_TTL)

    return products


def get_categories_queryset():
    CATEGORIES_CACHE_KEY = "categories"
    CATEGORIES_TTL = 60 * 60 * 24 * 7

    categories = cache.get(CATEGORIES_CACHE_KEY)

    if not categories:
        categories = [category.name for category in Category.objects.all()]
        cache.set(CATEGORIES_CACHE_KEY, categories, CATEGORIES_TTL)

    return categories
