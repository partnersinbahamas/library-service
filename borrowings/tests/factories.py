from datetime import timedelta

import factory
from django.utils import timezone

from borrowings.models import Borrowing
from library.tests.factories import BookFactory
from user.tests.factories import UserFactory


class BorrowingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Borrowing

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)

    borrow_date = factory.LazyFunction(lambda: timezone.now().date())

    expected_return_date = factory.LazyAttribute(
        lambda obj: obj.borrow_date + timedelta(days=14)
    )

    return_date = None
