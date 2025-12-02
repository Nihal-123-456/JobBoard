from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job, JobApplication
from .models import Education, WorkExperience
from accounts.forms import JobSeekerProfileForm
from django.contrib.auth import get_user_model
from .forms import JobApplicationForm, EducationForm, WorkExperienceForm

User = get_user_model()

# Create your views here.
@login_required
def jobseeker_dashboard(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can access the Job Seeker Dashboard.")
        return redirect("landing")

    applications = request.user.applications.select_related("job").order_by("-applied_at")

    return render(request, "jobseekers/jobseeker_dashboard.html", {
        "applications": applications,
    })

@login_required
def apply_job(request, job_id):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("landing")

    job = get_object_or_404(Job, id=job_id)

    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect("job-detail", job_id=job.id)

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            messages.success(request, "Your application has been submitted successfully!")
            return redirect("jobseeker-dashboard")
    else:
        form = JobApplicationForm(initial={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        })

    return render(request, "jobseekers/apply_job.html", {"form": form, "job": job})

@login_required
def withdraw_application(request, job_id):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can withdraw applications.")
        return redirect("landing")

    job = get_object_or_404(Job, id=job_id)
    application = JobApplication.objects.filter(job=job, applicant=request.user).first()

    if not application:
        messages.warning(request, "You have not applied for this job.")
        return redirect("job-detail", job_id=job.id)

    if request.method == "POST":
        application.delete()

    messages.success(request, "You have successfully withdrawn your application.")
    return redirect("jobseeker-dashboard")

@login_required
def jobseeker_profile(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Access denied.")
        return redirect("landing")

    user = request.user
    educations = Education.objects.filter(user=user)
    experiences = WorkExperience.objects.filter(user=user)

    if request.method == "POST":
        form = JobSeekerProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("jobseeker-profile")
    else:
        form = JobSeekerProfileForm(instance=user)

    context = {
        "form": form,
        "educations": educations,
        "experiences": experiences,
    }
    return render(request, "jobseekers/profile.html", context)

@login_required
def add_education(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Access denied.")
        return redirect("landing")

    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()
            messages.success(request, "Education added successfully!")
            return redirect("jobseeker-profile")
    else:
        form = EducationForm()

    return render(request, "jobseekers/add_education.html", {"form": form})

@login_required
def add_experience(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Access denied.")
        return redirect("landing")

    if request.method == "POST":
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, "Work experience added successfully!")
            return redirect("jobseeker-profile")
    else:
        form = WorkExperienceForm()

    return render(request, "jobseekers/add_experience.html", {"form": form})

@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, id=pk, user=request.user)
    edu.delete()
    messages.success(request, "Education deleted.")
    return redirect("jobseeker-profile")

@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(WorkExperience, id=pk, user=request.user)
    exp.delete()
    messages.success(request, "Work experience deleted.")
    return redirect("jobseeker-profile")

@login_required
def preview_profile(request):
    if request.user.role != "job_seeker":
        messages.error(request, "Only job seekers can preview their profile.")
        return redirect("landing")

    user = request.user
    educations = Education.objects.filter(user=user)
    experiences = WorkExperience.objects.filter(user=user)

    context = {
        "applicant": user,
        "educations": educations,
        "experiences": experiences,
    }

    return render(request, "jobseekers/preview_profile.html", context)

@login_required
def edit_education(request, pk):
    if request.user.role != "job_seeker":
        messages.error(request, "Access Denied.")
        return redirect("landing")

    education = get_object_or_404(Education, id=pk, user=request.user)

    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully!")
            return redirect("jobseeker-profile")
    else:
        form = EducationForm(instance=education)

    return render(request, "jobseekers/edit_education.html", {"form": form})


@login_required
def edit_experience(request, pk):
    if request.user.role != "job_seeker":
        messages.error(request, "Access Denied.")
        return redirect("landing")

    experience = get_object_or_404(WorkExperience, id=pk, user=request.user)

    if request.method == "POST":
        form = WorkExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Work experience updated successfully!")
            return redirect("jobseeker-profile")
    else:
        form = WorkExperienceForm(instance=experience)

    return render(request, "jobseekers/edit_experience.html", {"form": form})