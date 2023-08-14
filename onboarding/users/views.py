"""User onboarding views."""
from django.db.utils import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from onboarding.users.models import MyUser, OneTimePin, verify_OTP
from onboarding.users.serializers import (
    MyUserSerializer,
    OneTimePinSerializer,
    OneTimePinVerificationSerializer,
    UserRegistrationSerializer,
)


class MyUserViewSet(viewsets.ModelViewSet):
    """User related viewsets."""

    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = MyUserSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        """User registration."""
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if validated_data["password"] != validated_data["confirm_password"]:
            return Response(
                {"confirm_password": "passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = MyUser.objects.create(
                identifier=validated_data["identifier"],
                identifier_type=validated_data["identifier_type"],
            )
            user.set_password(validated_data["password"])
            user.save()
        except IntegrityError:
            return Response(
                {"user": "user with the same identifier exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": f"{user}",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )

    @action(detail=False, methods=["post"])
    def otp(self, request):
        """Send OTP to user for onboarding verification."""
        serializer = OneTimePinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        OTP = OneTimePin.objects.create(
            identifier=validated_data["identifier"],
            identifier_type=validated_data["identifier_type"],
        )
        OTP.save()
        return Response({"one_time_PIN": "sent successfully"})

    @action(detail=False, methods=["post"])
    def verify_otp(self, request):
        """Verify OTP for user onboarding."""
        serializer = OneTimePinVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        verified = verify_OTP(
            validated_data["code"],
            validated_data["identifier"],
            validated_data["identifier_type"],
        )
        return Response({"verification": verified})


class CustomTokenObtainPairView(TokenObtainPairView):
    """Customized token generation view."""

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class CustomTokenRefreshPairView(TokenRefreshView):
    """Customized token refresh view."""

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class OneTimePinViewSet(viewsets.ModelViewSet):
    """OTP related viewsets."""

    pass
