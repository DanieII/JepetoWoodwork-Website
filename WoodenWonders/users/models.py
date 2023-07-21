from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("Either email or phone number must be provided.")
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email, phone_number=phone_number, password=password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email or str(self.phone_number)
