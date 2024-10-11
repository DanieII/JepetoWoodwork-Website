from django.core.validators import ValidationError


def only_alpha(value):
    if not all([x.isalpha() for x in value]):
        raise ValidationError("Полето трябва да съдържа само букви")
