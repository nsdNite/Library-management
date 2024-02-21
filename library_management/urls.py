from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("books.urls", namespace="books")),
    path("api/", include("borrowing_service.urls", namespace="borrowings")),
    path("user/", include("user.urls", namespace="user")),
]
