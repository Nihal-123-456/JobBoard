from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    major = models.CharField(max_length=255, blank=True, null=True)
    passing_year = models.PositiveIntegerField()
    result = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_experiences")
    institution = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_currently_there = models.BooleanField(default=False)
    responsibilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.institution}"