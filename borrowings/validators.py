from django.utils import timezone
from rest_framework.exceptions import ValidationError


class ValidateBorrowingExpectedReturnDate:
    def __call__(self, attrs):
        borrow_date = attrs.get("borrow_date", timezone.now().date())
        expected_return_date = attrs.get("expected_return_date")

        if expected_return_date and expected_return_date < borrow_date:
            raise ValidationError("Expected return date cannot be before borrow date.")


class ValidateBorrowingReturnDate:
    def __call__(self, attrs):
        borrow_date = attrs.get("borrow_date", timezone.now().date())
        return_date = attrs.get("return_date")

        if return_date and return_date < borrow_date:
            raise ValidationError("Return date cannot be before borrow date.")


class ValidateBookInventory:
    def __call__(self, attrs):
        book = attrs.get("book", None)

        if book.inventory <= 0:
            raise ValidationError("Book is out of stock.")
