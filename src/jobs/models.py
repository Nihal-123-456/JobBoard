from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from helpers import cloudinary_init

cloudinary_init()

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Job(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def get_display_name(instance, *args, **kwargs):
    if instance.full_name:
        return f'resume-of-{instance.full_name}'
    return 'user-resume'

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()

    resume = CloudinaryField(resource_type='raw', display_name=get_display_name, 
    tags=["user", "resume", "jobseeker"], 
    public_id_prefix="user_resume",
    allowed_formats=['pdf', 'doc', 'docx', 'odt', 'txt', 'rtf'],
    folder='jobseeker_resumes', overwrite=True)
    
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"