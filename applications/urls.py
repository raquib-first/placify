from django.urls import path

from .views import (
    apply_job,
    job_applicants,
    update_application_status,
    )

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('job/<int:job_id>/applicants/', job_applicants, name='job_applicants'),
    path('application/<int:app_id>/<str:status>/', update_application_status,name='update_application_status')
]
