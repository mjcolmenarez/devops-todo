from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    # Force input and display format: MM/DD/YYYY
    due_date = forms.DateField(
        required=False,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
                # keep type="text" so browsers don't force YYYY-MM-DD
                'type': 'text',
                'placeholder': 'MM/DD/YYYY',
                'pattern': r'\d{2}/\d{2}/\d{4}',
                'title': 'Use MM/DD/YYYY, e.g., 09/30/2025',
                'autocomplete': 'off',
            }
        )
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_done']
        labels = {
            'due_date': 'Due date (MM/DD/YYYY)',
        }

