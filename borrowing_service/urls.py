from rest_framework.routers import DefaultRouter

from borrowing_service.views import BorrowingViewSet

router = DefaultRouter()
router.register(r"", BorrowingViewSet)

urlpatterns = router.urls

app_name = "borrowing_service"
