from rest_framework.routers import DefaultRouter

from books.views import BookViewSet, BorrowingViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"borrowings", BorrowingViewSet)

urlpatterns = router.urls

app_name = "books"
