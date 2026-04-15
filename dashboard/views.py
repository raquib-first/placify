from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application
from profiles.models import StudentProfile, CompanyProfile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta


@login_required
def student_dashboard(request):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student_profile = request.user.studentprofile
    applications = Application.objects.filter(student=student_profile)

    applied_jobs = (
        student_profile.applications
        .select_related('job', 'job__company')
        .order_by('-applied_at')[:4]
    )

    total_applications = applications.count()
    accepted_count = applications.filter(status="SHORTLISTED").count()
    rejected_count = applications.filter(status="REJECTED").count()
    pending_count = (total_applications-(accepted_count + rejected_count ))

    last_7_days = timezone.now() - timedelta(days=7)
    recent_applications = applications.filter(applied_at__gte=last_7_days).count()

    context = {
        'student_profile': student_profile,
        'applications': applications,
        'completion': student_profile.completion_percentage(),
        'notifications': request.user.notifications.all(),
        'applied_jobs': applied_jobs,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'recent_applications': recent_applications,
    }

    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def company_dashboard(request):
    try:
        company = request.user.companyprofile
    except ObjectDoesNotExist:
        return redirect('create_company_profile')

    jobs = Job.objects.filter(company=company)

    applications_count = { job.id: job.applications.count() for job in jobs }

    total_jobs = jobs.count()

    total_applications = Application.objects.filter(
        job__company=company
    ).count()

    pending_applications = Application.objects.filter(
        job__company=company,
        status="PENDING"
    ).count()

    accepted_applications = Application.objects.filter(
        job__company=company,
        status="ACCEPTED"
    ).count()

    rejected_applications = Application.objects.filter(
        job__company=company,
        status="REJECTED"
    ).count()

    from django.db.models import Count
    most_applied_job = jobs.annotate(
        app_count=Count('applications')
    ).order_by('-app_count').first()

    return render(request, "dashboard/company_dashboard.html", {
        "company": company,
        "jobs": jobs,
        "applications_count": applications_count,
        "completion": company.completion_percentage(),
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "accepted_applications": accepted_applications,
        "rejected_applications": rejected_applications,
        "most_applied_job": most_applied_job,
    })
