"""Users model instance test cases."""
import time

import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker

from config import settings
from onboarding.users.models import MyUser, OneTimePin, verify_OTP

pytestmark = pytest.mark.django_db


@pytest.fixture
def phone_number_user():
    """Create test phone numberuser."""
    return baker.make(
        MyUser,
        identifier="+254711223344",
        identifier_type="PHONE_NUMBER",
    )


@pytest.fixture
def email_user():
    """Create test email user."""
    return baker.make(
        MyUser,
        identifier="myuser@email.com",
        identifier_type="EMAIL",
    )


def test_phone_number_user_creation(phone_number_user):
    """Verify creation of a phone number user."""
    users = MyUser.objects.all()
    assert users.count() == 1

    user = users.first()
    assert user == phone_number_user
    assert str(phone_number_user) == "+254711223344"
    assert user.identifier == "+254711223344"
    assert user.identifier_type == "PHONE_NUMBER"


def test_email_user_creation(email_user):
    """Verify creation of a email user."""
    users = MyUser.objects.all()
    assert users.count() == 1

    user = users.first()
    assert user == email_user
    assert str(email_user) == "myuser@email.com"
    assert user.identifier == "myuser@email.com"
    assert user.identifier_type == "EMAIL"


def test_phone_number_user_with_invalid_number():
    """Verify validation of phone number user."""
    with pytest.raises(ValidationError) as e:
        baker.make(
            MyUser,
            identifier="myuser@email.com",
            identifier_type="PHONE_NUMBER",
        )
    assert e
    assert "The phone number entered is not valid." in e.value.message


def test_email_user_with_invalid_email():
    """Verify validation of email user."""
    with pytest.raises(ValidationError) as e:
        baker.make(
            MyUser,
            identifier="71122334455",
            identifier_type="EMAIL",
        )
    assert e
    assert "Enter a valid email address." in e.value.message


def test_one_time_pin():
    """Verify sending of a one time PIN."""
    baker.make(
        OneTimePin,
        identifier="myuser@email.com",
        identifier_type="EMAIL",
    )

    assert OneTimePin.objects.count() == 1


def test_verify_one_time_pin():
    """Test verification of an OTP."""
    otp = baker.make(
        OneTimePin,
        identifier="myuser@email.com",
        identifier_type="EMAIL",
    )
    assert otp.valid
    assert str(otp) == otp.code

    verified = verify_OTP(otp.code, otp.identifier, otp.identifier_type)
    otp.refresh_from_db()
    assert verified
    assert not otp.valid


def test_expired_one_time_pin():
    """Verify OTP expiration."""
    otp = baker.make(
        OneTimePin,
        identifier="myuser@email.com",
        identifier_type="EMAIL",
    )
    assert otp.valid

    time.sleep(settings.OTP_VALIDITY_SECONDS + 1)
    verified = verify_OTP(otp.code, otp.identifier, otp.identifier_type)
    otp.refresh_from_db()
    assert not verified
    assert not otp.valid


def test_non_existent_one_time_pin():
    """Test verification of a non-existent OTP."""
    otp = baker.make(
        OneTimePin,
        identifier="myuser@email.com",
        identifier_type="EMAIL",
    )

    verified = verify_OTP("123456", otp.identifier, otp.identifier_type)
    assert not verified
