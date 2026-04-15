from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from .forms import StudentProfileForm, CompanyProfileForm, ProjectForm
from .models import StudentProfile, CompanyProfile, Project
from django.shortcuts import render, get_object_or_404
from jobs.models import Job
from django.core.exceptions import PermissionDenied
from applications.models import Application

@login_required
def company_public_profile(request, company_id):
    company = get_object_or_404(
        CompanyProfile.objects.select_related("user"),
        id=company_id
    )

    jobs = Job.objects.filter(company=company).order_by("-created_at")

    # ✅ Decide base template
    if hasattr(request.user, "companyprofile") and request.user.companyprofile.id == company.id:
        base_template = "base_company.html"   # own profile → show navbar
    else:
        base_template = "base_public.html"    # public view → no navbar

    return render(request, "profiles/company_public_profile.html", {
        "profile": company,
        "jobs": jobs,
        "completion": company.completion_percentage() if hasattr(company, "completion_percentage") else 0,
        "base_template": base_template
    })

@login_required
def student_public_profile(request, student_id=None):

    # ✅ CASE 1: Own profile
    if student_id is None:
        profile = get_object_or_404(StudentProfile, user=request.user)
        projects = Project.objects.filter(user=profile.user)

        base_template = "base.html"  # own profile → show navbar

        return render(request, 'profiles/student_public_profile.html', {
            'profile': profile,
            'projects': projects,
            'skills_list': [s.strip() for s in profile.skills.split(',')] if profile.skills else [],
            'base_template': base_template
        })

    # ✅ CASE 2: Other student
    profile = get_object_or_404(StudentProfile, user_id=student_id)
    projects = Project.objects.filter(user=profile.user)

    # 🔒 Student block
    if hasattr(request.user, 'studentprofile') and request.user != profile.user:
        raise PermissionDenied("You cannot view other student profiles.")

    # 🔒 Company check
    if hasattr(request.user, 'companyprofile'):
        has_applied = Application.objects.filter(
            student__user_id=student_id,
            job__company=request.user.companyprofile
        ).exists()

        if not has_applied:
            raise PermissionDenied("This student did not apply to your job.")

    # 🔒 Profile privacy
    if not profile.is_public and request.user != profile.user:
        raise PermissionDenied("This profile is private.")

    # 🔒 Project visibility
    if profile.project_visibility == 'private' and request.user != profile.user:
        projects = []

    elif profile.project_visibility == 'recruiters':
        if not hasattr(request.user, 'companyprofile'):
            projects = []

    # ✅ Decide base template
    if hasattr(request.user, "studentprofile") and request.user.studentprofile.user == profile.user:
        base_template = "base.html"   # own profile
    else:
        base_template = "base_public.html"  # public view

    return render(request, 'profiles/student_public_profile.html', {
        'profile': profile,
        'projects': projects,
        'skills_list': [s.strip() for s in profile.skills.split(',')] if profile.skills else [],
        'base_template': base_template
    })

@login_required
def profile_detail(request):
    user = request.user
    profile = None
    template = 'profiles/unknown.html'
    completion = 0
    jobs = None  

    if user.role == 'STUDENT':
        profile = StudentProfile.objects.filter(user=user).first()
        template = 'profiles/student_profile.html'

    elif user.role == 'COMPANY':
        profile = CompanyProfile.objects.filter(user=user).first()
        template = 'profiles/company_profile.html'

        if profile:
            jobs = profile.jobs.order_by('-created_at') 

    if profile:
        completion = profile.completion_percentage()

    return render(
        request,
        template,
        {
            'profile': profile,
            'completion': completion,
            'jobs': jobs  
        }
    )


@login_required
def company_profile_edit(request):
    user = request.user
    # Only companies can edit this
    if not hasattr(user, 'role') or user.role != 'COMPANY':
        return redirect('/')  # redirect non-company users

    # Get or create company profile
    profile, created = CompanyProfile.objects.get_or_create(user=user)

    previous_url = request.GET.get('next') or request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:company_dashboard')  # goes to prev page
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, 'profiles/company_profile_edit.html', {
        'form': form,
        'profile': profile , # pass profile for completion bar
        'next': previous_url,
    })


@login_required
def student_profile_edit(request):
    user = request.user

    # Only students allowed
    if not hasattr(user, 'role') or user.role != 'STUDENT':
        return redirect('/')

    # Get or create student profile
    profile, created = StudentProfile.objects.get_or_create(user=user)

    previous_url = request.GET.get('next') or request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard:student_dashboard')
            # or: return redirect(previous_url)

    else:
        form = StudentProfileForm(instance=profile)

    return render(
        request,
        'profiles/student_profile_edit.html',
        {
            'form': form,
            'profile': profile,
            'next': previous_url,
        }
    )

@login_required
def manage_resume(request):
    profile = request.user.studentprofile 
    return render(request, 'profiles/view_resume.html', {
        'profile': profile
    })

@login_required
def user_projects(request):
    projects = Project.objects.filter(user=request.user)
    
    return render(request, 'profiles/user_project.html', {
        'projects': projects
    })

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user   # VERY IMPORTANT
            project.save()
            return redirect('profiles:projects')

    else:
        form = ProjectForm()

    return render(request, 'profiles/add_project.html', {
        'form': form
    })

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('profiles:projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'profiles/edit_project.html', {
        'form': form
    })

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        project.delete()
        return redirect('profiles:projects')

    return render(request, 'profiles/delete_project.html', {
        'project': project
    })

@login_required
def privacy_settings(request):
    user = request.user

    # Detect profile type
    if hasattr(user, 'studentprofile'):
        profile = user.studentprofile
        is_student = True
    elif hasattr(user, 'companyprofile'):
        profile = user.companyprofile
        is_student = False
    else:
        return redirect('/')

    if request.method == 'POST':
        profile.is_public = 'is_public' in request.POST
        profile.show_email = 'show_email' in request.POST

        if is_student:
            profile.project_visibility = request.POST.get('project_visibility')

        profile.save()
        return redirect('profiles:privacy_settings')

    if request.user.is_authenticated:
        if request.user.role == request.user.Role.COMPANY:
            base_template = "base_company.html"
        else:
            base_template = "base.html"
    else:
        base_template = "base_public.html"

    return render(request, 'profiles/privacy_settings.html', {
        'base_template': base_template,
        'profile': profile,
        'is_student': is_student
    })

from django.contrib import messages

def help_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(request, "Your message has been sent!")
        return redirect('profiles:help')

    # 🔥 Dynamic base template logic
    if request.user.is_authenticated:
        if request.user.role == request.user.Role.COMPANY:
            base_template = "base_company.html"
        else:
            base_template = "base.html"
    else:
        base_template = "base_public.html"

    return render(request, 'profiles/help_page.html', {
        'base_template': base_template
    })

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_403(request, exception):
    return render(request, "403.html", status=403)

def custom_500(request):
    return render(request, "500.html", status=500)