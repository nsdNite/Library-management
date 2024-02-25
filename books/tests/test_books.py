from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from user.models import User

BOOKS_URL = reverse("books:book-list")

NEW_BOOK_DATA = {
    "title": "New Book",
    "author": "New Author",
    "inventory": 5,
    "cover": Book.CoverType.HARD,
    "daily_fee": "15.00",
}

UPDATE_BOOK_DATA = {
    "title": "Updated Title",
    "author": "Updated Author",
    "inventory": 15,
    "cover": Book.CoverType.SOFT,
    "daily_fee": "12.00",
}


class UnauthenticatedBorrowingListTests(TestCase):
    """Tests if unauthorized user have access to book list"""

    def setUp(self):
        self.client = APIClient()

    def test_no_auth_required(self):
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class BookPermissionsTestCase(TestCase):
    """Tests if non-admin user is unable to create, update and delete books"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.com", password="test_password_0451"
        )

        self.book = Book.objects.create(
            title="Test book",
            author="Test author",
            inventory=10,
            cover=Book.CoverType.SOFT,
            daily_fee=0.10,
        )

        self.admin = User.objects.create_superuser(
            email="test@admin.com",
            password="test_password_0451",
        )

    def test_standard_user_permissions(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post("/api/books/", NEW_BOOK_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(f"/api/books/{self.book.id}/", UPDATE_BOOK_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_permissions(self):
        client = APIClient()
        client.force_authenticate(user=self.admin)

        response = client.post("/api/books/", NEW_BOOK_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.put(f"/api/books/{self.book.id}/", UPDATE_BOOK_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
