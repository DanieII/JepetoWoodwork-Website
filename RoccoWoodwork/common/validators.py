from django.core.validators import ValidationError
from django.contrib.auth.password_validation import MinimumLengthValidator


def only_letters_validator(value):
    if not all([x.isalpha() for x in value]):
        raise ValidationError("Това поле трябва да съдържа само букви")


class CustomMinLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                "Паролата трябва да съдържа поне 8 символа.",
                code="password_too_short",
                params={"min_length": self.min_length},
            )
