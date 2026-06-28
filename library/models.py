from django.core.validators import MaxValueValidator
from django.db import models

from library.choices import BookCoverChoices
from library.utils import get_current_year


class Book(models.Model):
    api_id = models.IntegerField(unique=True, default=None, null=True)
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    summaries = models.TextField(blank=True, null=True)
    cover = models.CharField(
        choices=BookCoverChoices.choices, default=BookCoverChoices.HARD, max_length=10
    )
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
