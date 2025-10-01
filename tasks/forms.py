from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    # MM/DD/YYYY for date
    due_date = forms.DateField(
        required=False,
        input_formats=["%m/%d/%Y"],
        widget=forms.DateInput(
            format="%m/%d/%Y",
            attrs={
                "type": "text",  # keep text so the browser doesn't force YYYY-MM-DD
                "placeholder": "MM/DD/YYYY",
                "pattern": r"\d{2}/\d{2}/\d{4}",
                "title": "Use MM/DD/YYYY, e.g., 09/30/2025",
                "autocomplete": "off",
            },
        ),
        label="Due date (MM/DD/YYYY)",
    )

    # 12-hour time like 10:00 PM
    due_time = forms.TimeField(
        required=False,
        input_formats=["%I:%M %p"],
        widget=forms.TextInput(
            attrs={
                "placeholder": "HH:MM AM/PM",
                "title": "Use 12-hour time, e.g., 10:00 PM",
                "autocomplete": "off",
            }
        ),
        label="Due time (optional, e.g., 10:00 PM)",
    )

    class Meta:
        model = Task
        # no 'is_done' on the form (you toggle it from the list)
        fields = ["title", "description", "status", "priority", "task_type", "due_date", "due_time"]

        widgets = {
            "status": forms.Select(),
            "priority": forms.Select(),
            "task_type": forms.Select(),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
