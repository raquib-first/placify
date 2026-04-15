from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from profiles.models import StudentProfile
from jobs.models import Job
from django.shortcuts import render
from .models import Application
from django.http import JsonResponse
from notifications.models import Notification
from notifications.views import mark_as_read


@login_required
def apply_job(request, job_id):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student = StudentProfile.objects.get(user=request.user)
    job = get_object_or_404(Job, id=job_id)

    Application.objects.get_or_create(
        student=student,
        job=job
    )
    Notification.objects.create(
    user=job.company.user,   # company owner
    title="New Job Application",
    message=f"{request.user.username} applied for {job.title}"
)
    return redirect('jobs:student_job_list')


@login_required
def job_applicants(request, job_id):
    if request.user.role != request.user.Role.COMPANY:
        return redirect('dashboard:student_dashboard')

    job = get_object_or_404(Job, id=job_id)

    # security check: company can see only its jobs
    if job.company.user != request.user:
        return redirect('dashboard:company_dashboard')

    applications = Application.objects.filter(job=job)

    return render(
        request,
        'applications/job_applicants.html',
        {
            'job': job,
            'applications': applications
        }
    )

@login_required
def update_application_status(request, app_id, status):
    if request.user.role != request.user.Role.COMPANY:
        return redirect('dashboard:student_dashboard')

    application = get_object_or_404(Application, id=app_id)

    # company ownership check
    if application.job.company.user != request.user:
        return redirect('jobs:company_jobs')

    if status not in ['ACCEPTED', 'REJECTED', 'SHORTLISTED']:
        return redirect('applications:job_applicants', job_id=application.job.id)

    application.status = status
    application.save()

    # 🔔 STUDENT NOTIFICATION
    if status == 'SHORTLISTED':
        Notification.objects.create(
            user=application.student.user,
            title="Application Accepted 🎉",
            message=(
                f"Congratulations! Your application for "
                f"{application.job.title} at "
                f"{application.job.company.user.username} has been accepted."
            )
        )

    elif status == 'REJECTED':
        Notification.objects.create(
            user=application.student.user,
            title="Application Rejected",
            message=(
                f"Your application for {application.job.title} at "
                f"{application.job.company.user.username} was rejected."
            )
        )

    return redirect('applications:job_applicants', job_id=application.job.id)
