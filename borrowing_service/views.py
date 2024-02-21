from django.db.backends.base.base.BaseDatabaseWrapper import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer

    @action(detail=False, methods=["get"])
    def get_borrowing_by_user_and_status(self, request):
        """Endpoint for getting borrowing by user id and active status"""
        user_id = request.query_params.get("user_id")
        is_active = request.query_params.get("is_active") == "true"

        queryset = self.get_queryset().filter(user_id=user_id)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        else:
            queryset = queryset.exclude(actual_return_date__isnull=True)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def return_book(self, request, pk=None):
        """Endpoint for returning borrowed book and setting actual return date to current date.
        Updates inventory of borrowed book by +1"""
        borrowing = self.get_object()
        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save(update_fields=["inventory"])

        serializer = self.get_serializer(borrowing)

        return Response(serializer.data)
