import pytest
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from library.choices import BookCoverChoices
from library.models import Book
from library.serializers import BookSerializer
from library.tests.factories import BookFactory
from user.tests.factories import UserFactory

BOOK_DEFAULT_ID = 1

BOOK_LIST_URL = reverse_lazy("library:books-list")
BOOK_DETAIL_URL = reverse_lazy("library:books-detail", args=[BOOK_DEFAULT_ID])


@pytest.mark.django_db
class TestBooksListView:
    def setup_method(self):
        self.client = APIClient()

    def test_unauthenticated_user_has_access_to_books_list(self):
        response = self.client.get(BOOK_LIST_URL)

        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_cannot_create_books(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        response = self.client.post(BOOK_LIST_URL, data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_user_cannot_create_books(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        response = self.client.post(BOOK_LIST_URL, data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_book(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        book_data = {
            "title": "Test Book",
            "f": "Test Summary",
            "author": "Test Author",
            "cover": BookCoverChoices.HARD.value,
            "inventory": 10,
            "daily_fee": 10.00,
            "year_of_publication": 2023,
        }

        response = self.client.post(BOOK_LIST_URL, data=book_data)

        book = Book.objects.get(id=response.data["id"])

        book_serializer = BookSerializer(instance=book)

        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == 1

        assert response.data == book_serializer.data


@pytest.mark.django_db
class TestBooksDetailView:
    def setup_method(self):
        self.client = APIClient()

    def test_unauthenticated_user_has_access_to_book_detail_view(self):
        BookFactory(id=BOOK_DEFAULT_ID)
        response = self.client.get(BOOK_DETAIL_URL)

        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_cannot_update_book(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        response = self.client.post(BOOK_DETAIL_URL, data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin_user_cannot_update_book(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        response = self.client.post(BOOK_DETAIL_URL, data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_book(self):
        user = UserFactory(admin=True)
        self.client.force_authenticate(user)

        BookFactory(id=BOOK_DEFAULT_ID, title="Test book title")

        update_data = {
            "title": "Test Book title updated",
        }

        response = self.client.patch(BOOK_DETAIL_URL, data=update_data)

        book = Book.objects.get(id=response.data["id"])

        book_serializer = BookSerializer(instance=book)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == book_serializer.data
        assert book.title == "Test Book title updated"
