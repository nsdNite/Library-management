from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
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
        return BorrowingSerializer

    # @action(detail=True, methods=["POST"])
    # def return_book(self, request, pk=None):
    #     """Endpoint for returning borrowed book and setting actual return date to current date.
    #     Updates inventory of borrowed book by +1"""
    #     borrowing = self.get_object()
    #     borrowing.actual_return_date = timezone.now()
    #     borrowing.save()
    #
    #     borrowing.book.inventory += 1
    #     borrowing.book.save(update_fields=["inventory"])
    #
    #     serializer = self.get_serializer(borrowing)
    #
    #     return Response(serializer.data)
