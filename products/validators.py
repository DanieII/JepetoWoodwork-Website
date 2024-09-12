from django.core.exceptions import ValidationError


def validate_first_character(value):
    if not value[0].isalpha():
        raise ValidationError('The product name must start with a letter')
