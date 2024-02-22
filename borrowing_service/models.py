from django.core.exceptions import ValidationError
from django.db import models, transaction

from datetime import datetime, date

from library_management import settings
from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, related_name="borrowings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrowings",
        on_delete=models.CASCADE,
    )

    def validate(self):
        current_date = datetime.now()
        borrow_date = datetime.date(current_date)
        if self.expected_return_date < borrow_date:
            raise ValidationError(
                "Expected return date must be after borrow date."
            )

        if self.actual_return_date and self.actual_return_date < borrow_date:
            raise ValidationError(
                "Actual return date must be after borrow date."
            )

    def clean(self):
        self.validate()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
