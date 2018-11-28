from django.db import models
from django.conf import settings


class DinnerDecider(models.Model):
    Monday = models.CharField(max_length=128)
    Tuesday = models.CharField(max_length=128)
    Wednesday = models.CharField(max_length=128)
    Thursday = models.CharField(max_length=128)
    Friday = models.CharField(max_length=128)
    Saturday = models.CharField(max_length=128)
    Sunday = models.CharField(max_length=128)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.Monday


class TodoList(models.Model):
    Task = models.CharField(max_length=128)
    Date = models.DateTimeField(auto_now=False, auto_now_add=False)
    Info = models.TextField(max_length=1024, null=True)
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.Task






