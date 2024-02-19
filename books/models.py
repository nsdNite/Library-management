from django.db import models

from enum import Enum


class CoverType(Enum):
    HARD = "Hard cover"
    SOFT = "Soft cover"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=125)
    cover = models.CharField(
        max_length=10, choices=[(tag, tag.value) for tag in CoverType]
    )
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=2, decimal_places=2)
