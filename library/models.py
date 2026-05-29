from django.core.validators import MaxValueValidator
from django.db import models

from library.choices import BookCoverChoices
from library.utils import get_current_year


class Book(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    author = models.CharField(max_length=100)
    cover = models.CharField(choices=BookCoverChoices.choices, max_length=10)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    year_of_publication = models.PositiveIntegerField(
        validators=[MaxValueValidator(get_current_year())]
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        verbose_name_plural = "Books"
        verbose_name = "Book"
        ordering = ["-year_of_publication"]
