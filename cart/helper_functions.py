from products.models import Product


def get_cart_products(session):
    return {
        Product.objects.get(slug=slug): quantity
        for slug, quantity in session.get("cart", {}).items()
    }


def get_total_price(products):
    total_price = 0

    for product, quantity in products.items():
        total_price += product.price * quantity

    return total_price


def process_cart_quantity(product_slug, product, quantity, cart, pre_order):
    cart[product_slug] += quantity

    if not pre_order:
        product.quantity -= cart[product_slug]

        if product.quantity < 0:
            cart[product_slug] += product.quantity

    return cart
