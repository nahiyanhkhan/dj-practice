from django.shortcuts import render
from .models import Task


# Create your views here.
def task_list(request):
    task_list = Task.objects.all()
    completed = request.GET.get("completed")
    if completed == "1":
        task_list = task_list.filter(completed=True)
    elif completed == "0":
        task_list = task_list.filter(completed=False)
    return render(request, "task_list.html", {"tasks": task_list})


def task(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "task_details.html", {"task": task})
