from django.contrib import admin
from .models import Task, TodoList

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "todo_list")
    list_filter = ("status", "priority", "task_type", "todo_list")
    search_fields = ("title", "description")


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    # Keep only guaranteed fields so there’s no SystemCheckError
    list_display = ("name",)
    search_fields = ("name",)
