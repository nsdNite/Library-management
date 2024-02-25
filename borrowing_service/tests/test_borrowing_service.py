from datetime import date

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowing_service.models import Borrowing
from user.models import User


BORROWINGS_URL = reverse("borrowing_service:borrowing-list")


class UnauthenticatedBorrowingListTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class BorrowingFilterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.com", password="test_password_0451"
        )

        self.admin = User.objects.create_superuser(
            email="test@admin.com",
            password="test_password_0451",
        )

        self.another_user = User.objects.create_user(
            email="another@example.com",
            password="password",
        )

        self.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            inventory=10,
            cover=Book.CoverType.SOFT,
            daily_fee=10.50,
        )
        self.book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            inventory=5,
            cover=Book.CoverType.HARD,
            daily_fee=15.00,
        )

        Borrowing.objects.create(
            borrow_date=date(2024, 2, 1),
            expected_return_date=date(2025, 2, 15),
            book=self.book1,
            user=self.user,
        )
        Borrowing.objects.create(
            borrow_date=date(2024, 1, 1),
            expected_return_date=date(2025, 1, 15),
            book=self.book2,
            user=self.user,
        )

        Borrowing.objects.create(
            borrow_date=date(2024, 2, 10),
            expected_return_date=date(2025, 2, 20),
            book=self.book1,
            user=self.another_user,
        )

    def test_filter_by_user(self):
        """Test if results are filtered by user"""
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get("/api/borrowings/?user_id=" + str(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)

        # Test filtering by another user's borrowings (should be empty for standard user)
        response = client.get("/api/borrowings/?user_id=" + str(self.admin.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 0)

    def test_filter_by_active_status(self):
        """Test if results are filtered by active status"""
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Test filtering by active borrowings (where actual_return_date is null)
        response = client.get("/api/borrowings/?is_active=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)

        # Mark one of the borrowings as returned
        borrowing = Borrowing.objects.filter(
            user=self.user, actual_return_date__isnull=True
        ).first()
        borrowing.actual_return_date = date.today()
        borrowing.save()

        # Test filtering again after marking a borrowing as returned
        response = client.get("/api/borrowings/?is_active=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_admin_can_view_all_borrowings(self):
        """Test if admin can"""
        client = APIClient()
        client.force_authenticate(user=self.admin)

        # Admin should be able to see all borrowings
        response = client.get("/api/borrowings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 3)


class BorrowingReturnTestCase(TestCase):
    def setUp(self):
        # Create a standard user
        self.user = User.objects.create_user(
            email="standard@example.com",
            password="password",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="password",
        )
        self.book = Book.objects.create(
            title="Book 1",
            author="Author 1",
            inventory=1,
            cover=Book.CoverType.SOFT,
            daily_fee=10.50,
        )

        self.borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 2, 1),
            expected_return_date=date(2025, 2, 15),
            book=self.book,
            user=self.user,
        )

    def test_return_book_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Test returning the borrowing
        response = client.post(f"/api/borrowings/{self.borrowing.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the borrowing has been returned
        updated_borrowing = Borrowing.objects.get(id=self.borrowing.id)
        self.assertIsNotNone(updated_borrowing.actual_return_date)

        # Check that the book's inventory has increased by 1
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.inventory, 2)
