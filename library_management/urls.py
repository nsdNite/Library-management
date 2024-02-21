from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from books.urls import router as book_router
from borrowing_service.urls import router as borrowing_router

router_main = DefaultRouter()
router_main.registry.extend(book_router.registry)
router_main.registry.extend(borrowing_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router_main.urls)),
    path("user/", include("user.urls", namespace="user")),
]
