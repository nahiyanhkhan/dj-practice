from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def hello_world(request):
    return HttpResponse("<h1>Hello World!</h1>")


def global_homepage(request):
    return HttpResponse("<h1>Hi from the global homepage!</h1>")


def homepage(request):
    data = {"title": "This is our homepage!!!", "content": "Home is love <3"}
    return render(request, "index.html", context=data)


def about(request):
    stack = "Django"
    return render(request, "about.html", {"stack": stack})


def greetings(request, person="Friend"):
    return render(request, "greetings.html", {"name": person})


def contact(request):
    email = "email@example.com"
    socials = [
        "Facebook: www.fb.com",
        "Instagram: www.ig.com",
        "Twitter: www.twitter.com",
        "Reddit: www.reddit.com",
    ]
    return render(request, "contact.html", {"email": email, "socials": socials})
