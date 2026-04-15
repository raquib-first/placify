from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'location',
            'job_type',
            'remote_type',
            'description',
            'required_experience',
            'skills',
            'qualifications',
            'responsibilities',
            'benefits',
            'salary',
            'application_deadline',
            'is_active',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
            'qualifications': forms.Textarea(attrs={'rows': 2}),
            'benefits': forms.Textarea(attrs={'rows': 2}),
            'application_deadline': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
