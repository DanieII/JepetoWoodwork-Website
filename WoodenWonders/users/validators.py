from django.core.exceptions import ValidationError


def city_validator(value):
    if not all([x.isalpha() for x in value]):
        raise ValidationError('The city can\'t contain numbers or special characters')
