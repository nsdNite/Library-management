from datetime import datetime


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)
from borrowing_service.telegram_notifications import send_telegram_notification


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        """Filter borrowings by user and by status(active)
        endpoint:

        GET /api/borrowings/?user_id=123&is_active=true

        Prohibits user to view other borrowings rather than his ows.
        Admin can view all borrowings
        """
        queryset = Borrowing.objects.all()
        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_book":
            return BorrowingReturnSerializer

        return BorrowingSerializer

    @action(detail=True, methods=["POST"], url_path="return")
    def return_book(self, request, pk=None):
        """Endpoint for returning borrowed book and setting actual return date to current date.
        Increases inventory of borrowed book by 1.
        Prohibits user to return non their books.
        """

        current_date = datetime.now()
        return_date = datetime.date(current_date)

        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)

        if borrowing.user != request.user:
            return Response(
                {
                    "detail": "You don't have permission to return this borrowing"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        borrowing.actual_return_date = return_date
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save(update_fields=["inventory"])

        message = f"Returned borrowing: {borrowing.book} - {borrowing.user} at {return_date}"
        send_telegram_notification(message)

        return Response(serializer.data)
