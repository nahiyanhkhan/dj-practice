from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("<int:pk>/", views.task, name="task_details"),
    path("add/", views.add_todo, name="add_todo"),
    path("delete/<int:pk>/", views.delete_todo, name="delete_todo"),
]
