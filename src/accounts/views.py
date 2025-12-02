from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import Notification
# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect("landing")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, "Account created successfully!")

            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(request, email=email, password=raw_password)
            login(request, user)

            if user.role == "employer":
                return redirect("employer-dashboard")
            return redirect("jobseeker-dashboard")

    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("landing")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)

                if user.role == "employer":
                    return redirect("employer-dashboard")
                else:
                    return redirect("jobseeker-dashboard")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def notifications_list(request):
    notes = request.user.notifications.order_by("-created_at")
    return render(request, "notifications/list.html", {"notifications": notes})

@login_required
def mark_notification_read(request, pk):
    note = get_object_or_404(Notification, id=pk, user=request.user)
    if request.method == "POST":
        note.is_read = True
        note.save()
        messages.success(request, "Notification marked as read.")
        return redirect("notifications")
    messages.error(request, "Access denied.")
    return redirect("landing")

@login_required
def delete_notification(request, pk):
    note = get_object_or_404(Notification, id=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Notification deleted.")
        return redirect("notifications")
    messages.error(request, "Access denied.")
    return redirect("landing")