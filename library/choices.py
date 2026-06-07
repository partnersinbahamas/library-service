from django.db import models


class BookCoverChoices(models.TextChoices):
    HARD = "hard", "Hard"
    SOFT = "soft", "Soft"
    EBOOK = "ebook", "E-Book"
