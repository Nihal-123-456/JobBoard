from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobForm
from jobs.models import Job
from django.contrib.auth import get_user_model
from jobs.models import JobApplication
from job_seekers.models import Education, WorkExperience
from accounts.models import Notification

User = get_user_model()

# Create your views here.
@login_required
def create_job(request):
    if request.user.role != 'employer':
        messages.error(request, "Only employers can create job listings.")
        return redirect("landing")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # assign employer automatically
            job.save()

            messages.success(request, "Job listing created successfully!")
            return redirect("employer-dashboard")
    else:
        form = JobForm()

    return render(request, "employers/create_job.html", {"form": form})

@login_required
def employer_dashboard(request):
    if request.user.role != "employer":
        messages.error(request, "Only employers can access the Employer Dashboard.")
        return redirect("landing")

    jobs = Job.objects.filter(employer=request.user).order_by("-date_posted")
    total_applications = JobApplication.objects.filter(job__employer=request.user).count()

    context = {
        "jobs": jobs, "total_applications": total_applications
    }
    return render(request, "employers/employer_dashboard.html", context)

@login_required
def update_job(request, job_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can edit job listings.")
        return redirect("landing")

    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect("employer-dashboard")
    else:
        form = JobForm(instance=job)

    return render(request, "employers/update_job.html", {"form": form, "job": job})

@login_required
def delete_job(request, job_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can delete job listings.")
        return redirect("landing")

    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect("employer-dashboard")

    return render(request, "employers/confirm_delete.html", {"job": job})

@login_required
def view_applications(request, job_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can view job applications.")
        return redirect("landing")

    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.select_related("applicant").order_by("-applied_at")

    return render(request, "employers/view_applications.html", {
        "job": job,
        "applications": applications
    })

@login_required
def view_applicant_profile(request, job_id, applicant_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can view profile of applicants.")
        return redirect("landing")

    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applicant = get_object_or_404(User, id=applicant_id, role="job_seeker")

    has_applied = JobApplication.objects.filter(job=job, applicant=applicant).exists()
    if not has_applied:
        messages.error(request, "Applicant did not apply to this job.")
        return redirect("landing")

    already_seen = Notification.objects.filter(
        user=applicant,
        actor=request.user,
        type=Notification.NOTIF_PROFILE_VIEW,
        related_job=job,
        related_applicant=applicant,
    ).exists()

    if not already_seen:
        Notification.objects.create(
            user=applicant,
            actor=request.user,
            type=Notification.NOTIF_PROFILE_VIEW,
            message=f"An employer has viewed your profile",
            related_job=job,
            related_applicant=applicant,
        )

    educations = Education.objects.filter(user=applicant)
    experiences = WorkExperience.objects.filter(user=applicant)

    return render(
        request,
        "jobseekers/preview_profile.html",
        {
            "applicant": applicant,
            "educations": educations,
            "experiences": experiences,
        },
    )
