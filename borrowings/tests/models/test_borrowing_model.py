import pytest
import time_machine
from django.core.exceptions import ValidationError

from borrowings.models import Borrowing
from borrowings.tests.factories import BorrowingFactory
from library.tests.factories import BookFactory
from user.tests.factories import UserFactory


@pytest.mark.django_db
class TestBorrowingModel:
    def test_borrowing_str_method(self):
        book = BookFactory()
        user = UserFactory()

        borrowing = BorrowingFactory(
            book=book,
            user=user,
        )

        f"Borrowing of {str(borrowing.book)} by {str(borrowing.user)}"

    @time_machine.travel("2026-01-05", tick=False)
    def test_borrowing_should_be_created(self):
        book = BookFactory()
        user = UserFactory()

        borrowing = BorrowingFactory(
            book=book,
            user=user,
            expected_return_date="2026-01-08",
            return_date="2026-01-10",
        )

        assert Borrowing.objects.count() == 1
        assert borrowing.book.id == book.id
        assert borrowing.user.id == user.id
        assert str(borrowing.borrow_date) == "2026-01-05"
        assert str(borrowing.expected_return_date) == "2026-01-08"
        assert str(borrowing.return_date) == "2026-01-10"

    @time_machine.travel("2026-01-05", tick=False)
    def test_should_validate_borrowing_expected_return_date(self):
        with pytest.raises(ValidationError) as exc:
            BorrowingFactory(
                expected_return_date="2026-01-04",
            )

        error = exc.value.message_dict["__all__"]

        assert Borrowing.objects.count() == 0
        assert "Expected return date cannot be before borrow date." in error

    @time_machine.travel("2026-01-05", tick=False)
    def test_should_validate_borrowing_return_date(self):
        with pytest.raises(ValidationError) as exc:
            BorrowingFactory(
                return_date="2026-01-04",
            )

        error = exc.value.message_dict["__all__"]

        assert Borrowing.objects.count() == 0
        assert "Return date cannot be before borrow date." in error

    def test_borrowing_unique_constraint(self):
        book = BookFactory()
        user = UserFactory()

        BorrowingFactory(book=book, user=user)

        with pytest.raises(ValidationError) as exc:
            BorrowingFactory(book=book, user=user)

        error = exc.value.message_dict["__all__"]

        assert Borrowing.objects.count() == 1
        assert "Constraint “unique_user_borrowing” is violated." in error
