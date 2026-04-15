from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from profiles.models import CompanyProfile
from .forms import JobForm
from .models import Job
from applications.models import Application, SavedJob
from django.contrib import messages

@login_required
def create_job(request):
    if request.user.role != request.user.Role.COMPANY:
        raise PermissionDenied

    company = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.is_active = True
            job.save()
            return redirect('jobs:company_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})

@login_required
def company_jobs(request):
    if request.user.role != request.user.Role.COMPANY:
        raise PermissionDenied

    company = get_object_or_404(CompanyProfile, user=request.user)
    jobs = Job.objects.filter(company=company)
    return render(request, 'jobs/company_jobs.html', {'jobs': jobs})


@login_required
def student_job_list(request):
    if request.user.role != request.user.Role.STUDENT:
        raise PermissionDenied

    # Get the student's profile
    student_profile = request.user.studentprofile

    # Only get applications for this student profile
    applied_job_ids = set(
        Application.objects.filter(student=student_profile)
        .values_list('job_id', flat=True)
    )
    saved_job_ids = set(
        SavedJob.objects.filter(student=student_profile)
        .values_list('job_id', flat=True)
    )

    jobs = Job.objects.exclude(id__in=applied_job_ids).order_by('-created_at')

    return render(request, 'jobs/student_job_list.html',{
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
        'saved_job_ids': saved_job_ids,
    })

@login_required
def edit_job(request, job_id):

    # ✅ check role first
    if request.user.role != request.user.Role.COMPANY:
        raise PermissionDenied

    # ✅ get company first
    company = get_object_or_404(CompanyProfile, user=request.user)

    # ✅ THEN get job
    job = get_object_or_404(Job, id=job_id, company=company)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()

            # ✅ SUCCESS MESSAGE
            messages.success(request, "Job updated successfully!")

            return redirect('jobs:company_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {
        'form': form,
        'job': job
    })

@login_required
def delete_job(request, job_id):

    if request.user.role != request.user.Role.COMPANY:
        raise PermissionDenied

    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, company=company)
    job.delete()

    return redirect('jobs:company_jobs')

@login_required
def save_job(request, job_id):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student = request.user.studentprofile
    job = get_object_or_404(Job, id=job_id, is_active=True)

    SavedJob.objects.get_or_create(
        student=student,
        job=job
    )

    return redirect(request.META.get('HTTP_REFERER', 'jobs:student_job_list'))


@login_required
def unsave_job(request, job_id):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student = request.user.studentprofile
    SavedJob.objects.filter(student=student, job_id=job_id).delete()

    return redirect(request.META.get('HTTP_REFERER', 'jobs:student_job_list'))

@login_required
def saved_jobs(request):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student = request.user.studentprofile

    applied_job_ids = set(
        Application.objects.filter(student=student)
        .values_list('job_id', flat=True)
    )

    saved_jobs = SavedJob.objects.filter(student=student)\
        .select_related('job', 'job__company')\
        .order_by('-saved_at')

    return render(request, 'jobs/saved_jobs.html', {
        'saved_jobs': saved_jobs,
        'applied_job_ids':applied_job_ids
    })

@login_required
def applied_jobs(request):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student = request.user.studentprofile

    applications = Application.objects.filter(
        student=student
    ).select_related('job', 'job__company').order_by('-applied_at')

    return render(request, 'jobs/applied_jobs.html', {
        'applications': applications
    })

@login_required
def company_view_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    # Default template
    base_template = "base_public.html"

    # If user is a company
    if request.user.role == request.user.Role.COMPANY:
        company = get_object_or_404(CompanyProfile, user=request.user)

        # Restrict access to only their jobs
        if job.company != company:
            return redirect('dashboard:company_dashboard')

        # If it's their own job → use company template
        base_template = "base_company.html"

    return render(request, "jobs/company_view_job.html", {
        "job": job,
        "base_template": base_template
    })

@login_required
def student_view_job(request, job_id):
    if request.user.role != request.user.Role.STUDENT:
        return redirect('dashboard:company_dashboard')

    student = request.user.studentprofile

    job = get_object_or_404(Job, id=job_id, is_active=True)

    # Check applied
    is_applied = Application.objects.filter(
        student=student,
        job=job
    ).exists()

    # Check saved
    is_saved = SavedJob.objects.filter(
        student=student,
        job=job
    ).exists()

    return render(request, "jobs/company_view_job.html", {
        "job": job,
        "is_applied": is_applied,
        "is_saved": is_saved,
    })

