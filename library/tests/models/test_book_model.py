import pytest

from library.choices import BookCoverChoices
from library.models import Book
from library.tests.factories import BookFactory


@pytest.mark.django_db
class TestBookModel:
    def test_book_should_be_created(self):
        book = BookFactory(
            api_id=1,
            title="Test Book",
            author="Test Author",
            summaries="Test Summary",
            cover=BookCoverChoices.HARD,
            inventory=10,
            daily_fee=10.00,
            year_of_publication=2023,
        )

        assert Book.objects.count() == 1

        assert book.api_id == 1
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.summaries == "Test Summary"
        assert book.cover == BookCoverChoices.HARD
        assert book.inventory == 10
        assert book.daily_fee == 10.00
        assert book.year_of_publication == 2023

    def test_book_str_method(self):
        book = BookFactory(title="Test Book", author="Test Author")

        assert str(book) == "Test Book by Test Author"
