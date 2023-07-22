"""Usersapp model instances."""
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import validate_email
from django.db import models
from phonenumber_field.validators import validate_international_phonenumber

from onboarding.users.managers import MyUserManager


class MyUser(AbstractBaseUser):
    """Custom user POC."""

    EMAIL = "EMAIL"
    PHONE_NUMBER = "PHONE_NUMBER"
    IDENTIFIER_TYPE_CHOICES = [
        (EMAIL, "Email"),
        (PHONE_NUMBER, "Phone number"),
    ]

    identifier = models.CharField(max_length=255, unique=True)
    identifier_type = models.CharField(
        max_length=255, choices=IDENTIFIER_TYPE_CHOICES
    )

    objects = MyUserManager()

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = ["identifier_type"]

    def __str__(self) -> str:
        """Human readable representation of a user."""
        return self.identifier

    def validate_identifier(self) -> None:
        """Validate the provided identifer, given their identifier type."""
        match self.identifier_type:
            case self.EMAIL:
                validate_email(self.identifier)
            case self.PHONE_NUMBER:
                validate_international_phonenumber(self.identifier)
            case _:
                pass

    def save(self):
        """Override default save method."""
        self.validate_identifier()
        return super().save()
