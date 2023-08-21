from django import template

register = template.Library()


@register.filter
def get_range_from_number(number):
    return range(number)
