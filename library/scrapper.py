import random

import requests

from library.utils import get_current_year

from .choices import BookCoverChoices
from .models import Book

GUTENDEX_BOOK_URL = "https://gutendex.com/books/"


def fetch_book_page(url: str):
    result = requests.get(url)
    return result.json()


def books_scrapper():
    next_page = GUTENDEX_BOOK_URL

    while next_page:
        books = []
        result = fetch_book_page(next_page)

        next_page = result.get("next")
        books_response = result.get("results")

        for book_response in books_response:
            book_id = book_response.get("id")
            is_book_already_in_db = Book.objects.filter(api_id=book_id).exists()

            if is_book_already_in_db:
                print(f"Character with id {book_id} already in the database.")
                continue

            book_authors = book_response.get("authors") or []

            authors = " & ".join([book_author["name"] for book_author in book_authors])

            """
                This is fake data, as api do not have a real publication year info,
                we take author death year as a potential book publication year or current year
            """

            death_year = None

            if book_authors:
                death_year = book_authors[0].get("death_year")
            year_of_publication = (
                death_year if death_year and death_year > 0 else get_current_year()
            )

            book = Book(
                api_id=book_id,
                title=book_response.get("title")[:255],
                summaries=" ".join(book_response.get("summaries")),
                cover=random.choice(BookCoverChoices.values),
                author=authors[:255],
                inventory=random.randrange(99),
                year_of_publication=year_of_publication,
                daily_fee=round(random.uniform(0, 49), 2),
            )

            books.append(book)

        Book.objects.bulk_create(books)
