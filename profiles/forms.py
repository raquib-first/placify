from django import forms
from .models import StudentProfile, CompanyProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'phone',
            'location',
            'university',
            'degree',
            'branch',
            'graduation_year',
            'cgpa',
            'headline',
            'bio',
            'skills',
            'github_url',
            'linkedin_url',
            'portfolio_url',
            'resume',
        ]


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'company_name',
            'website',
            'industry',
            'company_size',
            'founded_year',
            'headquarters',
            'description',
            'hr_name',
            'hr_email',
            'linkedin_page',
        ]

from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack', 'github_link', 'live_link']