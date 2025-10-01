from django import forms
from .models import Task, TodoList


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "MM/DD/YYYY"})
    )
    due_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={"placeholder": "HH:MM"})
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "task_type",
            "due_date",
            "due_time",
            "todo_list",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Task title"}),
            "description": forms.Textarea(attrs={"rows": 8, "placeholder": "Description"}),
        }


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "List name"})}
