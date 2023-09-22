from products.models import Product
from django.core.cache import cache


def get_products_queryset():
    cache_key = "products"
    products_ttl = 60 * 60 * 24 * 7
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.all()
        cache.set(cache_key, products, products_ttl)

    return products


def get_last_viewed_products(session):
    products = get_products_queryset()
    return [products.get(slug=slug) for slug in session.get("last_viewed")]
