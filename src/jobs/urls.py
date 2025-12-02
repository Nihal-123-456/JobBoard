from django.urls import path
from .views import job_listings, job_detail

urlpatterns = [
    path("", job_listings, name="job-listings"),
    path("<int:job_id>/", job_detail, name="job-detail"),
]
