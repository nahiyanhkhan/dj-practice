from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("myapp.urls")),
    path("", include("myapp.urls")),
    path("tasks/", include("todo_app.urls")),
]
