from pickletools import read_uint1
from re import escape
from django.shortcuts import render, redirect

import todo_app
from .models import Task
from .forms import SearchForm, AddTodoForm
from django.http import HttpResponse
from django.urls import reverse


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
