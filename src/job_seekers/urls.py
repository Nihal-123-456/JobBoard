from django.urls import path
from .views import jobseeker_dashboard, apply_job, withdraw_application, jobseeker_profile, add_education,add_experience, delete_education, delete_experience, preview_profile, edit_education, edit_experience

urlpatterns = [
    path("dashboard/", jobseeker_dashboard, name="jobseeker-dashboard"),
    path("<int:job_id>/apply/", apply_job, name="apply-job"),
    path("<int:job_id>/withdraw/", withdraw_application, name="withdraw-application"),
    path("profile/", jobseeker_profile, name="jobseeker-profile"),
    path("profile/add-education/", add_education, name="add-education"),
    path("profile/add-experience/", add_experience, name="add-experience"),
    path("profile/delete-education/<int:pk>/", delete_education, name="delete-education"),
    path("profile/delete-experience/<int:pk>/", delete_experience, name="delete-experience"),
    path("profile/edit-education/<int:pk>/", edit_education, name="edit-education"),
    path("profile/edit-experience/<int:pk>/", edit_experience, name="edit-experience"),
    path("profile/preview/", preview_profile, name="preview-profile"),
]
