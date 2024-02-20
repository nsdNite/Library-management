from rest_framework import viewsets

from books.models import Book, Borrowing
from books.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BorrowingSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # permission_classes = [IsAuthenticated]
    # pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        return BookSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
