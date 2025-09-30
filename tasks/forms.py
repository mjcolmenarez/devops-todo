from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    # Force input + display format: MM/DD/YYYY
    due_date = forms.DateField(
        required=False,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                'type': 'text',  # keep text so browsers don't force YYYY-MM-DD
                'placeholder': 'MM/DD/YYYY',
                'pattern': r'\d{2}/\d{2}/\d{4}',
                'title': 'Use MM/DD/YYYY, e.g., 09/30/2025',
                'autocomplete': 'off',
            },
        ),
    )

    class Meta:
        model = Task
        # Removed 'is_done' so the checkbox doesn't appear on the form
        fields = ['title', 'description', 'due_date']
        labels = {
            'due_date': 'Due date (MM/DD/YYYY)',
        }
