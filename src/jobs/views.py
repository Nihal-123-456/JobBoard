from django.shortcuts import render, get_object_or_404
from .models import Job, JobApplication, JobCategory
from django.contrib.auth import get_user_model

User = get_user_model()

def job_listings(request):
    category_id = request.GET.get("category")
    jobs = Job.objects.all().order_by("-date_posted")
    categories = JobCategory.objects.all()

    if category_id:
        jobs = jobs.filter(category_id=category_id)

    return render(request, "jobs/job_listings.html", {
        "jobs": jobs,
        "categories": categories
    })

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False

    if request.user.is_authenticated and request.user.role == "job_seeker":
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()

    context = {
        "job": job,
        "has_applied": has_applied
    }
    return render(request, "jobs/job_detail.html", context)