from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


BORROWINGS_URL = reverse("borrowing_service:borrowing-list")


class UnauthenticatedBorrowingListTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
