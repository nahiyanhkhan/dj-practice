from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", default=1
    )

    def __str__(self):
        return self.title


# class Author(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     bio = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# class Book(models.Model):
#     title = models.CharField(max_length=250)
#     description = models.TextField()
#     pub_date = models.DateField(null=True, blank=True)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

#     def __str__(self):
#         return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    pub_date = models.DateField(null=True, blank=True)
    author = models.ManyToManyField(Author, related_name="books")

    def __str__(self):
        return self.title
