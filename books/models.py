from django.db import models


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
    daily_fee = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"
