# Generated by Django 4.2.9 on 2024-02-19 10:55

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=125)),
                (
                    "cover",
                    models.CharField(
                        choices=[
                            (books.models.CoverType["HARD"], "Hard cover"),
                            (books.models.CoverType["SOFT"], "Soft cover"),
                        ],
                        max_length=10,
                    ),
                ),
                ("inventory", models.PositiveIntegerField(default=0)),
                (
                    "daily_fee",
                    models.DecimalField(decimal_places=2, max_digits=2),
                ),
            ],
        ),
    ]