from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path(
        "api/borrowings/",
        include("borrowing_service.urls", namespace="borrowing_service"),
    ),
    path("api/books/", include("books.urls", namespace="books")),
]
