from django.core.exceptions import ValidationError
from django.db import models, transaction

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

    def clean(self):
        if self.expected_return_date < self.borrow_date:
            return ValidationError(
                "Expected return date cannot be before borrowing date."
            )

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                self.book.inventory -= 1
                self.book.save(update_fields=["inventory"])
        super().save(*args, **kwargs)
