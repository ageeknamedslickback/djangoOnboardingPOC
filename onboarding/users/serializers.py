"""User app serializers."""
from rest_framework import serializers

from onboarding.users.models import MyUser, OneTimePin


class UserRegistrationSerializer(serializers.Serializer):
    """Custom user registration serializer."""

    identifier = serializers.CharField(max_length=255)
    identifier_type = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)


class MyUserSerializer(serializers.ModelSerializer):
    """MyUser model serializer class."""

    class Meta:
        """Serializer meta options."""

        model = MyUser
        fields = ("identifier", "identifier_type", "password")


class OneTimePinSerializer(serializers.ModelSerializer):
    """OTP model serializer."""

    class Meta:
        """Serializer meta options."""

        model = OneTimePin
        fields = ("identifier", "identifier_type")


class OneTimePinVerificationSerializer(serializers.Serializer):
    """One Time PIn verification serializer."""

    identifier = serializers.CharField(max_length=255)
    identifier_type = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=6)
