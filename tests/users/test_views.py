"""Users app views test cases."""
import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from onboarding.users.models import MyUser, OneTimePin

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    """Test user."""
    user = baker.make(
        MyUser,
        identifier="+254710234567",
        identifier_type="PHONE_NUMBER",
    )

    user.set_password("admin")
    user.save()

    return user


@pytest.fixture
def client():
    """Test client."""
    client = APIClient()
    return client


@pytest.fixture
def client_with_credentials(user):
    """Authenticate test client."""
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


def test_obtain_pair_view_without_authentication(client):
    """Verify obtain token endpoint."""
    url = reverse("token_obtain_pair")
    data = {
        "identifier": "+254710234567",
        "password": "admin",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == 401


def test_obtain_pair_view(client_with_credentials, user):
    """Verify obtain token endpoint."""
    url = reverse("token_obtain_pair")
    data = {
        "identifier": "+254710234567",
        "password": "admin",
    }

    response = client_with_credentials.post(url, data, format="json")
    assert response.status_code == 200

    data = response.json()
    assert data["refresh"]
    assert data["access"]


def test_register_user(client_with_credentials):
    """Verify registration of a new user."""
    url = reverse("user-register")
    payload = {
        "identifier": "+254700999888",
        "identifier_type": "PHONE_NUMBER",
        "password": "admin",
        "confirm_password": "admin",
    }
    response = client_with_credentials.post(url, payload, format="json")
    assert response.status_code == 200

    data = response.json()
    assert data["user"] == "+254700999888"
    assert data["access"]
    assert data["refresh"]


def test_register_user_with_passwords_not_matching(client_with_credentials):
    """Verify registration of a user with passwords not matching."""
    url = reverse("user-register")
    payload = {
        "identifier": "+254700999888",
        "identifier_type": "PHONE_NUMBER",
        "password": "admin",
        "confirm_password": "not-admin",
    }
    response = client_with_credentials.post(url, payload, format="json")
    assert response.status_code == 400

    data = response.json()
    assert data == {"confirm_password": "passwords do not match"}


def test_register_existing_user(client_with_credentials):
    """Verify creation of an existing user."""
    url = reverse("user-register")
    payload = {
        "identifier": "+254710234567",
        "identifier_type": "PHONE_NUMBER",
        "password": "admin",
        "confirm_password": "admin",
    }
    response = client_with_credentials.post(url, payload, format="json")
    assert response.status_code == 400

    data = response.json()
    assert data == {"user": "user with the same identifier exists"}


def test_send_registration_otp(client_with_credentials):
    """Verify sending of a registration OTP."""
    url = reverse("user-otp")
    payload = {
        "identifier": "+254700999888",
        "identifier_type": "PHONE_NUMBER",
    }
    response = client_with_credentials.post(url, payload, format="json")
    assert response.status_code == 200

    data = response.json()
    assert data == {"one_time_PIN": "sent successfully"}


def test_verify_registration_otp(client_with_credentials):
    """Verify OTP verification."""
    otp = baker.make(
        OneTimePin,
        identifier="+254700999888",
        identifier_type="PHONE_NUMBER",
    )

    url = reverse("user-verify-otp")
    payload = {
        "identifier": "+254700999888",
        "identifier_type": "PHONE_NUMBER",
        "code": otp.code,
    }
    response = client_with_credentials.post(url, payload, format="json")
    assert response.status_code == 200

    data = response.json()
    assert data == {"verification": True}


def test_verify_invalid_registration_otp(client_with_credentials):
    """Verify OTP verification."""
    url = reverse("user-verify-otp")
    payload = {
        "identifier": "+254700999888",
        "identifier_type": "PHONE_NUMBER",
        "code": "12345",
    }
    response = client_with_credentials.post(url, payload, format="json")
    assert response.status_code == 200

    data = response.json()
    assert data == {"verification": False}
