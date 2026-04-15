from django.urls import path
from .views import (profile_detail,  
            company_public_profile,  
            company_profile_edit, 
            company_public_profile,
            student_profile_edit,
            student_public_profile, 
            manage_resume,
            user_projects,
            add_project,
            edit_project,
            delete_project,
            privacy_settings,
            help_page
            )
app_name = "profiles"

urlpatterns = [
    path('me/', profile_detail, name='profile'),
    path("company/<int:company_id>/", company_public_profile, name="company_public_profile"),
    path('company/edit/', company_profile_edit, name='company_profile_edit'),
    path('student/edit/', student_profile_edit, name='student_profile_edit'),
    path('company/detail/', profile_detail, name='profile_detail'),
    path('student/detail/',profile_detail, name='student_profile'),
    path("company/<int:company_id>/", company_public_profile, name="company_public_profile"),
    path('student/public-profile/',student_public_profile,name='my_public_profile'),
    path('student/<int:student_id>/',student_public_profile,name='student_public_profile'),
    path('manage_resume/', manage_resume, name='manage_resume'),
    path('projects/', user_projects, name='projects'),
    path('projects/add/', add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('settings/privacy/', privacy_settings, name='privacy_settings'),
    path('help/', help_page, name='help'),
]
