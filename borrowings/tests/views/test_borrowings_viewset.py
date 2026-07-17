import pytest
import time_machine
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from borrowings.models import Borrowing
from borrowings.tests.factories import BorrowingFactory
from library.tests.factories import BookFactory
from user.tests.factories import UserFactory

BORROWINGS_URL = reverse_lazy("borrowings:borrowings-list")


@pytest.mark.django_db
class TestBorrowingsListView:
    def setup_method(self):
        self.client = APIClient()

    def test_unauthenticated_user_cannot_access_borrowings_list(self):
        response = self.client.get(BORROWINGS_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_see_only_own_borrowings(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        user_2 = UserFactory()

        BorrowingFactory(user=user_2)
        borrowing = BorrowingFactory(user=user)

        response = self.client.get(BORROWINGS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"] == [
            {
                "id": borrowing.id,
                "book": borrowing.book.id,
                "borrow_date": str(borrowing.borrow_date),
                "expected_return_date": str(borrowing.expected_return_date),
                "return_date": None,
                "user": user.id,
            }
        ]


@pytest.mark.django_db
class TestBorrowingsCreateView:
    def setup_method(self):
        self.client = APIClient()

    def test_unauthenticated_user_cannot_create_borrowings(self):
        response = self.client.post(BORROWINGS_URL, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @time_machine.travel("2026-01-05", tick=False)
    def test_should_validate_borrowing_expected_return_date(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        book = BookFactory()

        data = {
            "book": book.id,
            "expected_return_date": "2026-01-04",
        }

        response = self.client.post(BORROWINGS_URL, data)

        assert (
            "Expected return date cannot be before borrow date."
            in response.data["non_field_errors"]
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @time_machine.travel("2026-01-05", tick=False)
    def test_should_validate_borrowing_return_date(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        book = BookFactory()

        data = {
            "book": book.id,
            "return_date": "2026-01-04",
        }

        response = self.client.post(BORROWINGS_URL, data)

        assert (
            "Return date cannot be before borrow date."
            in response.data["non_field_errors"]
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_validate_book_inventory(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        book = BookFactory(inventory=0)

        data = {
            "book": book.id,
        }

        response = self.client.post(BORROWINGS_URL, data)

        assert "Book is out of stock." in response.data["non_field_errors"]
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @time_machine.travel("2026-01-05", tick=False)
    def test_borrowing_should_be_created(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        book = BookFactory()

        data = {
            "book": book.id,
            "expected_return_date": "2026-02-03",
        }

        response = self.client.post(BORROWINGS_URL, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Borrowing.objects.count() == 1
