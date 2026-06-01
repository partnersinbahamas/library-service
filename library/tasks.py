from celery import shared_task

from .models import Book
from .scrapper import books_scrapper


@shared_task
def count_books():
    return Book.objects.count()


@shared_task
def sync_books():
    return books_scrapper()
