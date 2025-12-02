from django.contrib import admin
from .models import Job, JobApplication, JobCategory
# Register your models here.

admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(JobCategory)
