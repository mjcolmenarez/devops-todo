from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_NOT_STARTED = "not_started"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, "Not started"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_DONE, "Done"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    TYPE_HOMEWORK = "homework"
    TYPE_WORK = "work"
    TYPE_PERSONAL = "personal"
    TYPE_OTHER = "other"
    TYPE_CHOICES = [
        (TYPE_HOMEWORK, "Homework"),
        (TYPE_WORK, "Work"),
        (TYPE_PERSONAL, "Personal"),
        (TYPE_OTHER, "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # kept for backward compatibility with your toggle button
    is_done = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_OTHER)

    # due date (MM/DD/YYYY) + optional time (e.g., 10:00 PM)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_done", "due_date", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # keep status and is_done in sync
        if self.status == self.STATUS_DONE:
            self.is_done = True
        else:
            # if someone unchecks is_done elsewhere, reflect it
            if not self.is_done:
                if self.status == self.STATUS_DONE:
                    self.status = self.STATUS_NOT_STARTED
            else:
                # is_done True but status not done – trust status over is_done
                self.status = self.STATUS_DONE
        super().save(*args, **kwargs)
