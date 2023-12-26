from django import template

register = template.Library()


@register.filter
def calculate_empty_stars(review_stars):
    return range(5 - review_stars)
