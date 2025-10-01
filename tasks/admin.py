from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "priority", "task_type", "due_date", "due_time", "created_at")
    list_filter = ("status", "priority", "task_type", "is_done")
    search_fields = ("title", "description")
