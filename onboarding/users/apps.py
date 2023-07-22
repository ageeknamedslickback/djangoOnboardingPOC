"""Users app config file."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """App config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "onboarding.users"
