from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import StudentRegistrationForm, CompanyRegistrationForm, EditAccountForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomPasswordChangeForm
from notifications.models import Notification 

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/student_register.html', {'form': form})


def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:company_dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/company_register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == User.Role.STUDENT:
            return reverse_lazy('dashboard:student_dashboard')
        elif user.role == User.Role.COMPANY:
            return reverse_lazy('dashboard:company_dashboard')
        return reverse_lazy('admin:index')


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            request.user.set_password(new_password)
            request.user.save()

            # 🔔 SEND NOTIFICATION
            Notification.objects.create(
                user=request.user,
                title="Password Changed",
                message="Your account password was successfully changed."
            )

            messages.success(request, "Password changed successfully. Please login again.")
            if request.user.role == request.user.Role.STUDENT:
                return redirect("accounts:login")
            else:
                return redirect("accounts:login")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})

@login_required
def edit_account(request):

    user = request.user
    old_email = user.email

    if request.method == "POST":
        form = EditAccountForm(request.POST, instance=user)

        if form.is_valid():
            updated_user = form.save()
            if old_email != updated_user.email:
                Notification.objects.create(
                    user=updated_user,
                    title="Email Updated",
                    message="Your account email was successfully updated."
                )

            messages.success(request, "Account updated successfully.")

            if user.role == user.Role.STUDENT:
                return redirect("dashboard:student_dashboard")
            else:
                return redirect("dashboard:company_dashboard")
    else:
        form = EditAccountForm(instance=user)

    return render(request, "accounts/student_edit_account.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('accounts:login')

