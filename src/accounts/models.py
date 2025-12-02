from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from jobs.models import Job

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    )

    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    headline = models.CharField(max_length=150, blank=True, null=True,
        help_text="A short headline like 'Frontend Developer' or 'Recent Computer Science Graduate'")

    USERNAME_FIELD = 'email'  # login with email
    REQUIRED_FIELDS = ['username']  

    @property
    def unread_notifications(self):
        return self.notifications.filter(is_read=False).count()
    
class Notification(models.Model):
    NOTIF_APPLICATION = "application"
    NOTIF_WITHDRAW = "withdraw"
    NOTIF_PROFILE_VIEW = "profile_view"

    NOTIF_TYPES = [
        (NOTIF_APPLICATION, "Application"),
        (NOTIF_WITHDRAW, "Withdraw"),
        (NOTIF_PROFILE_VIEW, "Profile View"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="notifications")
    
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="actor_notifications")
    
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=40, choices=NOTIF_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_job = models.ForeignKey( Job, on_delete=models.SET_NULL,          null=True, blank=True, related_name="+")
    related_applicant = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="+")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification({self.user}, {self.type})"