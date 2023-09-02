from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email=None, phone_number=None, password=None, commit=True, **extra_fields
    ):
        if not email and not phone_number:
            raise ValueError(
                "Трябва да бъде въведен поне един имейл или телефонен номер."
            )

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)

        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        user = self.create_user(
            email=email, password=password, commit=False, **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        error_messages={"invalid": "Въведете валиден телефонен номер"},
    )
    date_joined = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.email or str(self.phone_number)
