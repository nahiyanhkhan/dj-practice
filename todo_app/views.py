from django.shortcuts import render, redirect
from .models import Task
from .forms import SearchForm, AddTodoForm
from django.http import HttpResponse


# Create your views here.
def task_list(request):
    task_list = Task.objects.all()
    completed = request.GET.get("completed")

    search_form = SearchForm(request.POST)

    if search_form.is_valid():
        query = search_form.cleaned_data.get("query")

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
    task = Task.objects.get(pk=pk)
    return render(request, "task_details.html", {"task": task})


def add_todo(request):
    # data = Task.objects.all()

    if request.method == "POST":
        add_todo_form = AddTodoForm(request.POST)
        if add_todo_form.is_valid():
            add_todo_form.save()
            return redirect("task_list")

    add_todo_form = AddTodoForm()

    context = {"add_todo_form": add_todo_form}

    return render(request, "add_todo.html", context=context)


def delete_todo(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect("task_list")
    except:
        return HttpResponse("Task does not exist!!!")
