from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone

from library.models import Book


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrowings")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="borrowings"
    )
    borrow_date = models.DateField()
    expected_return_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Borrowing of {self.book} by {self.user}"

    def clean(self):
        borrow_date = self.borrow_date or timezone.now().date()

        if self.return_date and self.return_date < borrow_date:
            raise ValidationError("Return date cannot be before borrow date.")

        if self.expected_return_date and self.expected_return_date < borrow_date:
            raise ValidationError("Expected return date cannot be before borrow date.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-borrow_date"]
        verbose_name = "Borrowing"
        verbose_name_plural = "Borrowings"
        indexes = [models.Index(fields=["book", "user", "return_date"])]
        constraints = (
            UniqueConstraint(
                fields=("book", "user"),
                condition=Q(return_date__isnull=True),
                name="unique_user_borrowing",
            ),
        )
