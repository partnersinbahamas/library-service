from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from borrowings.models import Borrowing
from library.models import Book


class BorrowingService:
    @staticmethod
    def book_borrow(book: Book, user: get_user_model(), **borrowing_data):
        with transaction.atomic():
            if Borrowing.objects.filter(
                book_id=book.id, user_id=user.id, return_date__isnull=True
            ).exists():
                raise ValidationError("Book is already borrowed.")

            if book.inventory <= 0:
                raise ValidationError("Book is out of stock.")

            borrowing = Borrowing.objects.create(book=book, user=user, **borrowing_data)

            book.inventory = F("inventory") - 1
            book.save()

            return borrowing
