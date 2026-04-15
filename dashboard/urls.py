from django.urls import path
from .views import student_dashboard, company_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('student/', student_dashboard, name='student_dashboard'),
    path('company/', company_dashboard, name='company_dashboard'),
]
