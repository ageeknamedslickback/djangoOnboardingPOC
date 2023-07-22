"""Users app model instances."""
import datetime
import math
import random

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.validators import validate_international_phonenumber

from config import settings
from onboarding.users import IDENTIFIER_TYPE_CHOICES
from onboarding.users.managers import MyUserManager


class AbstractBaseIdentifier(models.Model):
    """Abstract identifier model."""

    identifier = models.CharField(max_length=255, unique=True)
    identifier_type = models.CharField(
        max_length=255, choices=IDENTIFIER_TYPE_CHOICES
    )

    def validate_identifier(self) -> None:
        """Validate the provided identifer, given their identifier type."""
        match self.identifier_type:
            case "PHONE_NUMBER":
                validate_international_phonenumber(self.identifier)

            case "EMAIL":
                validate_email(self.identifier)

        return

    def save(self, *args, **kwargs) -> None:
        """Override default save method."""
        self.validate_identifier()
        return super().save(*args, **kwargs)

    class Meta:
        """Model meta options."""

        abstract = True


class MyUser(AbstractBaseUser, AbstractBaseIdentifier):
    """Custom user POC."""

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = ["identifier_type"]

    def __str__(self) -> str:
        """Human readable representation of a user."""
        return self.identifier


class OneTimePin(AbstractBaseIdentifier):
    """One time PIN used for user identifiers verification."""

    timestamp = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)
    code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self) -> str:
        """Human readable representation of a user."""
        return self.code

    def generate_OTP(self) -> str:
        """Generate the OTP code."""
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]

        return OTP

    def send_OTP(self) -> bool:
        """Send an OTP to the provided identifer."""
        match self.identifier_type:
            case "EMAIL":
                raise NotImplementedError("Email Not Implemented")

            case "PHONE_NUMBER":
                raise NotImplementedError("SMS Not Implemented")

    def save(self, *args, **kwargs) -> None:
        """Override default save method."""
        if not self.__class__.objects.filter(code=self.code):
            OTP = self.generate_OTP()
            self.code = OTP

        super().save(*args, **kwargs)


def verify_OTP(code: str, identifier: str, identifier_type: str) -> bool:
    """Verfiy an OTP code."""
    is_valid = False
    now = timezone.now()
    try:
        OTP = OneTimePin.objects.get(
            code=code,
            valid=True,
            identifier=identifier,
            identifier_type=identifier_type,
        )
        if now <= OTP.timestamp + datetime.timedelta(
            seconds=settings.OTP_VALIDITY_SECONDS
        ):
            is_valid = True

        OTP.valid = False
        OTP.save()
        return is_valid

    except OneTimePin.DoesNotExist:
        return False
