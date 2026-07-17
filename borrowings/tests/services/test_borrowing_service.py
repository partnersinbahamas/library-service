import pytest
import time_machine
from django.core.exceptions import ValidationError

from borrowings.models import Borrowing
from borrowings.services import BorrowingService
from borrowings.tests.factories import BorrowingFactory
from library.tests.factories import BookFactory
from user.tests.factories import UserFactory


@pytest.mark.django_db
class TestBorrowingService:
    def test_should_validate_borrowing_existence(self):
        user = UserFactory()
        book = BookFactory()

        BorrowingFactory(
            user=user,
            book=book,
        )

        with pytest.raises(ValidationError) as exc:
            BorrowingService.book_borrow(book, user)

        error = exc.value.error_list[0]

        assert "Book is already borrowed." in error.message

    @time_machine.travel("2026-01-05", tick=False)
    def test_should_not_validate_borrowing_existence_if_book_was_returned(self):
        user = UserFactory()
        book = BookFactory()

        BorrowingFactory(
            user=user,
            book=book,
            return_date="2026-01-06",
        )

        borrowing = BorrowingService.book_borrow(book, user)

        assert borrowing.user == user
        assert borrowing.book == book
        assert borrowing.return_date is None

    def test_should_validate_book_inventory(self):
        user = UserFactory()
        book = BookFactory(inventory=0)

        with pytest.raises(ValidationError) as exc:
            BorrowingService.book_borrow(book, user)

        error = exc.value.error_list[0]

        assert "Book is out of stock." in error.message

    def test_borrowing_should_be_created(self):
        user = UserFactory()
        book = BookFactory(inventory=1)

        borrowing = BorrowingService.book_borrow(book, user)

        assert Borrowing.objects.count() == 1
        assert borrowing.user == user
        assert borrowing.book == book
        assert book.inventory == 0
