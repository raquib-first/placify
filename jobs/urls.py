from django.urls import path
from .views import (
    create_job,
    company_jobs, 
    student_job_list, 
    edit_job, 
    delete_job, 
    saved_jobs, 
    applied_jobs, 
    save_job, 
    unsave_job,
    company_view_job,
    student_view_job
    )

app_name = 'jobs'

urlpatterns = [
    path('create/', create_job, name='create_job'),
    path('company/jobs/', company_jobs, name='company_jobs'),
    path('student/jobs/', student_job_list, name='student_job_list'),
    path('edit/<int:job_id>/', edit_job, name='edit_job'),
    path('delete/<int:job_id>/', delete_job, name='delete_job'),
    path('save/<int:job_id>/', save_job, name='save_job'),
    path('unsave/<int:job_id>/', unsave_job, name='unsave_job'),
    path('saved/', saved_jobs, name='saved_jobs'),
    path('applied/', applied_jobs, name='applied_jobs'),
    path("job/<int:job_id>/company/", company_view_job, name="company_view_job"),
    path("job/<int:job_id>/student/", student_view_job, name="student_view_job"),
]
