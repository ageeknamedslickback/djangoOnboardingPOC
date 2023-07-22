"""Users model instance test cases."""
import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker

from onboarding.users.models import MyUser

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
    assert users.first() == phone_number_user
    assert str(phone_number_user) == "+254711223344"


def test_email_user_creation(email_user):
    """Verify creation of a email user."""
    users = MyUser.objects.all()
    assert users.count() == 1
    assert users.first() == email_user
    assert str(email_user) == "myuser@email.com"


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
