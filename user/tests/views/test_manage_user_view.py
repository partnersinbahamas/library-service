import pytest

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from user.tests.factories import UserFactory

MANAGE_USER_URL = reverse_lazy("user:me")

@pytest.mark.django_db
class TestManageUserView:
    def setup_method(self):
        self.client = APIClient()


    def test_with_authenticated_user(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        response = self.client.get(MANAGE_USER_URL)

        assert response.status_code == status.HTTP_200_OK


    def test_permission_denied(self):
        response = self.client.get(MANAGE_USER_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
