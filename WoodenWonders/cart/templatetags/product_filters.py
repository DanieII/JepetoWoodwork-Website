from django import template

register = template.Library()


@register.filter
def calculate_total_price(price, quantity):
    return f"{price * quantity:.2f}"
