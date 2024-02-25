from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from books.urls import router as book_router
from borrowing_service.urls import router as borrowing_router

router_main = DefaultRouter()
router_main.registry.extend(book_router.registry)
router_main.registry.extend(borrowing_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router_main.urls)),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
