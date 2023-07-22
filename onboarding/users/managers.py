"""User app custom manager."""
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, identifier, identifier_type, password=None):
        """Create and save a User with the given identifiers."""
        if not identifier or not identifier_type:
            raise ValueError("Users must have an identifier or its type")

        match identifier_type:
            case "EMAIL":
                identifier = self.normalize_email(identifier)
            case _:
                pass

        user = self.model(
            identifier=identifier,
            identifier_type=identifier_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, identifier_type, password=None):
        """Create and save a superuser with the given identifiers."""
        user = self.create_user(
            identifier=identifier,
            password=password,
            identifier_type=identifier_type,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
