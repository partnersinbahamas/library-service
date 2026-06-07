import factory.django

from library.choices import BookCoverChoices
from library.models import Book
from library.utils import get_current_year


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    api_id = factory.Faker("pyint")
    title = factory.Faker("sentence")
    author = factory.Faker("name")
    summaries = factory.Faker("text")

    cover = factory.Iterator(
        [BookCoverChoices.HARD, BookCoverChoices.SOFT, BookCoverChoices.EBOOK]
    )

    inventory = factory.Faker("random_int", min=0, max=100)
    daily_fee = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
    )

    year_of_publication = factory.Faker(
        "random_int",
        min=999,
        max=get_current_year(),
    )
