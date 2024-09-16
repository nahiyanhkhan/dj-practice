from asyncio import tasks
from email.quoprimime import body_check
from pickletools import read_uint1
from pyexpat import model
from re import escape
from tracemalloc import take_snapshot
from turtle import title
from unittest import result
from django.shortcuts import render, redirect

import todo_app
from .models import Task, Author, Book
from .forms import SearchForm, AddTodoForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


# Create your views here.
def task_list(request):
    task_list = Task.objects.all()
    completed = request.GET.get("completed")

    search_form = SearchForm(request.POST)

    if search_form.is_valid():
        query = search_form.cleaned_data.get("query")
    else:
        return HttpResponse("Invalid search query")

    if completed == "1":
        task_list = task_list.filter(completed=True)
    elif completed == "0":
        task_list = task_list.filter(completed=False)

    if query:
        searched_task_list = [
            task for task in task_list if query.lower() in task.title.lower()
        ]
        task_list = searched_task_list

    context = {
        "tasks": task_list,
        "search_form": search_form,
    }

    return render(request, "task_list.html", context=context)


def task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        return render(request, "task_details.html", {"task": task})
    except Task.DoesNotExist:
        # 'home' is the fallback URL name
        previous_page = request.META.get("HTTP_REFERER", reverse("task_list"))
        message = """
        <h1>Task does not exist!!!</h1>
        <p><a href="{}">Go back to the previous page</a></p>
        """.format(
            previous_page
        )
        return HttpResponse(message)
        # return HttpResponse("Task does not exist!!!")


def add_todo(request):
    # data = Task.objects.all()

    if request.method == "POST":
        add_todo_form = AddTodoForm(request.POST)
        if add_todo_form.is_valid():
            add_todo_form.save()
            return redirect("task_list")
        else:
            return HttpResponse("Invalid form data")
            # return render(request, "add_todo.html", {"add_todo_form": add_todo_form})

    add_todo_form = AddTodoForm()

    context = {"add_todo_form": add_todo_form}

    return render(request, "add_todo.html", context=context)


def delete_todo(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect("task_list")
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist!!!")


def update_todo(request, pk):
    # return HttpResponse("Update Todo " + str(pk))
    try:
        task = Task.objects.get(pk=pk)

        if request.method == "POST":
            todo_form = AddTodoForm(request.POST, instance=task)
            if todo_form.is_valid():
                todo_form.save()
                return redirect("task_list")
            else:
                return render(request, "update_todo.html", {"todo_form": todo_form})

        todo_form = AddTodoForm(instance=task)
        return render(request, "update_todo.html", {"todo_form": todo_form})

    except Task.DoesNotExist:
        return HttpResponse("Task does not exist!!!")


def task_by_user_id(request, user_id):
    # --------------------------------------------
    # Type-1
    # tasks = Task.objects.filter(user_id=user_id).values()
    # return JsonResponse({"tasks": list(tasks)})
    # --------------------------------------------
    # Type-2
    # tasks = Task.objects.filter(user_id=user_id)
    # results = []
    # for task in tasks:
    #     results.append(
    #         {
    #             "title": task.title,
    #             "user_id": task.user.id,
    #             "username": task.user.username,
    #         }
    #     )
    # return JsonResponse({"tasks": list(results)})
    # --------------------------------------------
    # Type-3
    user = User.objects.get(pk=user_id)
    # tasks = user.tasks_set.all().values()
    tasks = user.tasks.all().values()
    return JsonResponse({"tasks": list(tasks)})


def all_books(request):
    books = Book.objects.all().values()
    return JsonResponse({"books": list(books)})


# def book(request, book_id):
#     book = Book.objects.get(id=book_id)
#     # return JsonResponse({"book": model_to_dict(book)})
#     book_details = {
#         "title": book.title,
#         "description": book.description,
#         "author": book.author.first_name + " " + book.author.last_name,
#     }
#     return JsonResponse({"book": book_details})


def author(request, author_id):
    author = Author.objects.get(id=author_id)
    author_details = {
        "first_name": author.first_name,
        "last_name": author.last_name,
        "bio": author.bio,
        "books": [book.title for book in author.books.all()],
    }
    return JsonResponse({"book": author_details})


# ---------- Many to Many ----------


def book(request, book_id):
    book = Book.objects.get(id=book_id)
    # return JsonResponse({"book": model_to_dict(book)})
    book_details = {
        "title": book.title,
        "description": book.description,
        "author": [
            author.first_name + " " + author.last_name for author in book.author.all()
        ],
    }
    return JsonResponse({"book": book_details})
