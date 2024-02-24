from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


BOOKS_URL = reverse("books:book-list")


class UnauthenticatedBorrowingListTests(TestCase):
    """Unauthorized user should have access to book list"""

    def setUp(self):
        self.client = APIClient()

    def test_no_auth_required(self):
        res = self.client.get(BOOKS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
