from django.core.exceptions import ValidationError


def city_validator(value):
    if not all([x.isalpha() for x in value]):
        raise ValidationError("Градът не може да съдържа числа или специални символи!")
