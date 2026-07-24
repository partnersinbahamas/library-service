from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing
from borrowings.validators import (
    ValidateBookInventory,
    ValidateBorrowingExpectedReturnDate,
    ValidateBorrowingReturnDate,
)
from library.models import Book


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "return_date",
            "user",
        )
        read_only_fields = ("id", "user")
        validators = [
            ValidateBorrowingExpectedReturnDate(),
            ValidateBorrowingReturnDate(),
            ValidateBookInventory(),
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        book = attrs.get("book", None)
        user = request.user

        if Borrowing.objects.filter(
            book_id=book.id, user_id=user.id, return_date__isnull=True
        ).exists():
            raise ValidationError("Book is already borrowed")

        return attrs


class BorrowingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "inventory")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BorrowingBookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "return_date",
            "user",
        )


class BorrowingRepaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "return_date",
            "user",
        )

    def validate(self, attrs):
        if self.instance and self.instance.return_date is not None:
            raise ValidationError("Book is already returned.")

        return attrs
