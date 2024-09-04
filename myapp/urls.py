from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello_world),
    path("home/", views.homepage),
    path("about/", views.about),
    path("contact/", views.contact),
    path("", views.global_homepage),
    path("greetings/", views.greetings),
    path("greetings/<person>", views.greetings),
]
