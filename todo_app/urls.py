from django.urls import path

from myapp import models
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("<int:pk>/", views.task, name="task_details"),
    path("add/", views.add_todo, name="add_todo"),
    path("delete/<int:pk>/", views.delete_todo, name="delete_todo"),
    path("update/<int:pk>/", views.update_todo, name="update_todo"),
    path("user/<int:user_id>/", views.task_by_user_id, name="task_user"),
    path("books/", views.all_books, name="all_books"),
    path("books/<int:book_id>", views.book, name="book"),
    path("author/<int:author_id>", views.author, name="author"),
    path("registration/", views.registration_view, name="registration"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
