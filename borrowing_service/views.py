from datetime import datetime


from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

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
        Increases inventory of borrowed book by 1."""

        current_date = datetime.now()
        return_date = datetime.date(current_date)

        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)

        borrowing.actual_return_date = return_date
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save(update_fields=["inventory"])

        return Response(serializer.data)
