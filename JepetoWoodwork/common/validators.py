from django.core.validators import ValidationError


def only_letters_validator(value):
    if not all([x.isalpha() for x in value]):
        raise ValidationError("This field should contain only letters")
