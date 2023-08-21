from products.models import Product


def get_last_viewed_products(session):
    return [Product.objects.get(slug=slug) for slug in session.get("last_viewed")]
