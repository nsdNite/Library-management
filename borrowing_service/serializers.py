from rest_framework import serializers

from books.serializers import BookDetailSerializer
from borrowing_service.models import Borrowing

from datetime import datetime


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

        read_only_fields = ("id", "borrow_date", "actual_return_date", "user")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Borrowing
        fields = ("id", "expected_return_date", "book", "user")

        read_only_fields = ("id", "user")

    def validate(self, data):
        """Validate next items:
        - expected return date is after borrowing date;
        - book is not out of stock."""
        current_date = datetime.now()
        borrow_date = datetime.date(current_date)
        if data["expected_return_date"] <= borrow_date:
            raise serializers.ValidationError(
                "Expected return date must be after borrow date."
            )

        book = data.get("book")
        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        return data

    def create(self, validated_data):
        """Create a new borrowing, lowering book's inventory by 1."""
        book = validated_data.get("book")
        book.inventory -= 1
        book.save()

        return Borrowing.objects.create(**validated_data)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )

    def validate(self, data):
        """Validate if actual return date is after borrowing date."""
        if self.instance.actual_return_date is not None:
            raise serializers.ValidationError(
                "This borrowing has been already returned!."
            )

        current_date = datetime.now()
        return_date = datetime.date(current_date)
        if self.instance.borrow_date > return_date:
            raise serializers.ValidationError(
                "Actual return date must be after borrow date."
            )

        return data
