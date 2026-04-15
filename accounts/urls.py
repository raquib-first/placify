from django.urls import path
from .views import student_register, company_register, CustomLoginView, user_logout, change_password,edit_account

app_name = 'accounts'

urlpatterns = [
    path('register/student/', student_register, name='student_register'),
    path('register/company/', company_register, name='company_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path("change-password/", change_password, name="change_password"),
    path("edit-account/", edit_account, name="edit_account"),
]