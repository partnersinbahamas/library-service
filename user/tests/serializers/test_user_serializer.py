import pytest

from user.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    def test_should_be_valid(self):
        data = {
            "username": "user",
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@library.com",
            "password": "my-password",
            "password_repeat": "my-password",
        }

        user_serializer = UserSerializer(data=data)

        assert user_serializer.is_valid()

    def test_should_validate_passwords_match(self):
        data = {
            "username": "user",
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@library.com",
            "password": "my-password",
            "password_repeat": "not-my-password",
        }

        user_serializer = UserSerializer(data=data)

        assert not user_serializer.is_valid()
        assert user_serializer.errors["non_field_errors"][0] == "Passwords do not match"
