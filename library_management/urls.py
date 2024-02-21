from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("books.urls", namespace="books")),
    path("api/", include("borrowing_service.urls", namespace="borrowings")),
    path("user/", include("user.urls", namespace="user")),
]
