from django.urls import path
from .views import employer_dashboard, create_job, update_job, delete_job, view_applicant_profile, view_applications

urlpatterns = [
    path("dashboard/", employer_dashboard, name="employer-dashboard"),
    path("job/create/", create_job, name="create-job"),
    path("job/<int:job_id>/edit/", update_job, name="update-job"),
    path("job/<int:job_id>/delete/", delete_job, name="delete-job"),
    path("job/<int:job_id>/applications/", view_applications, name="view-applications"),
    path("job/<int:job_id>/applicant/<int:applicant_id>/profile/", view_applicant_profile, name="view-applicant-profile"),
]
