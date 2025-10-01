from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_lists")
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        unique_together = ("user", "name")

    def __str__(self) -> str:
        return self.name


PRIORITY_CHOICES = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
]

STATUS_CHOICES = [
    ("not_started", "Not started"),
    ("in_progress", "In progress"),
    ("done", "Done"),
]

TASK_TYPE_CHOICES = [
    ("homework", "Homework"),
    ("other", "Other"),
]


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    todo_list = models.ForeignKey(
        TodoList, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_started")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, blank=True)

    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # IMPORTANT: do not use legacy fields like "is_done"
        ordering = ["status", "due_date", "title"]

    def __str__(self) -> str:
        return self.title
