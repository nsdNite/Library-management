from django.db import models

from library_management import settings


class Book(models.Model):

    class CoverType(models.TextChoices):
        HARD = "Hard cover"
        SOFT = "Soft cover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=125)
    inventory = models.PositiveIntegerField(default=0)
    cover = models.CharField(
        max_length=10, choices=CoverType.choices, default=CoverType.SOFT
    )
    daily_fee = models.DecimalField(max_digits=2, decimal_places=2)


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(
        Book, related_name="borrowings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrowings",
        on_delete=models.CASCADE,
    )
